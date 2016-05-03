/* Soot - a J*va Optimization Framework
 * Copyright (C) 1997-2000 Etienne Gagnon.
 * Copyright (C) 2008 Ben Bellamy 
 * Copyright (C) 2008 Eric Bodden 
 * 
 * All rights reserved.
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

/*
 * Modified by the Sable Research Group and others 1997-1999.  
 * See the 'credits' file distributed with Soot for the complete list of
 * contributors.  (Soot is distributed at http://www.sable.mcgill.ca/soot)
 */

package soot.jimple.toolkits.typing;

import soot.*;
import soot.options.*;
import soot.jimple.*;
import java.util.*;

/**
 * This transformer assigns types to local variables.
 * @author Etienne Gagnon
 * @author Ben Bellamy
 * @author Eric Bodden 
 */
public class TypeAssigner extends BodyTransformer {
	private boolean ignoreWrongStaticNess;

	public TypeAssigner(Singletons.Global g) {
	}

	public static TypeAssigner v() {
		return G.v().soot_jimple_toolkits_typing_TypeAssigner();
	}
	
	public boolean ignoreWrongStaticNess() {
		return ignoreWrongStaticNess;
	}

	/** Assign types to local variables. * */
	protected void internalTransform(Body b, String phaseName, Map options) {
		if (b == null) {
			throw new NullPointerException();
		}

		Date start = new Date();

		if (Options.v().verbose())
			G.v().out.println("[TypeAssigner] typing system started on "
					+ start);

		JBTROptions opt = new JBTROptions(options);
		
		ignoreWrongStaticNess = opt.ignore_wrong_staticness();
		
		/*
		 * Setting this guard to true enables comparison of the original and new
		 * type assigners. This will be slow since type assignment will always
		 * happen twice. The actual types used for Jimple are determined by the
		 * use-old-type-assigner option.
		 * 
		 * Each comparison is written as a separate semicolon-delimited line to
		 * the standard output, and the first field is always 'cmp' for use in
		 * grep. The format is:
		 * 
		 * cmp;Method Name;Stmt Count;Old Inference Time (ms); New Inference
		 * Time (ms);Typing Comparison
		 * 
		 * The Typing Comparison field compares the old and new typings: -2 -
		 * Old typing contains fewer variables (BAD!) -1 - Old typing is tighter
		 * (BAD!) 0 - Typings are equal 1 - New typing is tighter 2 - New typing
		 * contains fewer variables 3 - Typings are incomparable (inspect
		 * manually)
		 * 
		 * In a final release this guard, and anything in the first branch,
		 * would probably be removed.
		 */
		if (opt.compare_type_assigners()) {
			compareTypeAssigners(b,opt.use_older_type_assigner());
		} else {
			if (opt.use_older_type_assigner())
				TypeResolver.resolve((JimpleBody) b, Scene.v());
			else
				(new soot.jimple.toolkits.typing.fast.TypeResolver(
						(JimpleBody) b)).inferTypes();
		}

		Date finish = new Date();
		if (Options.v().verbose()) {
			long runtime = finish.getTime() - start.getTime();
			long mins = runtime / 60000;
			long secs = (runtime % 60000) / 1000;
			G.v().out.println("[TypeAssigner] typing system ended. It took "
					+ mins + " mins and " + secs + " secs.");
		}

		if (typingFailed((JimpleBody) b))
			throw new RuntimeException("type inference failed!");
	}

	private void compareTypeAssigners(Body b, boolean useOlderTypeAssigner) {
		JimpleBody jb = (JimpleBody) b, oldJb, newJb;
		int size = jb.getUnits().size();
		long oldTime, newTime;
		if (useOlderTypeAssigner) {
			// Use old type assigner last
			newJb = (JimpleBody) jb.clone();
			newTime = System.currentTimeMillis();
			(new soot.jimple.toolkits.typing.fast.TypeResolver(newJb))
					.inferTypes();
			newTime = System.currentTimeMillis() - newTime;
			oldTime = System.currentTimeMillis();
			TypeResolver.resolve(jb, Scene.v());
			oldTime = System.currentTimeMillis() - oldTime;
			oldJb = jb;
		} else {
			// Use new type assigner last
			oldJb = (JimpleBody) jb.clone();
			oldTime = System.currentTimeMillis();
			TypeResolver.resolve(oldJb, Scene.v());
			oldTime = System.currentTimeMillis() - oldTime;
			newTime = System.currentTimeMillis();
			(new soot.jimple.toolkits.typing.fast.TypeResolver(jb))
					.inferTypes();
			newTime = System.currentTimeMillis() - newTime;
			newJb = jb;
		}

		int cmp;
		if (newJb.getLocals().size() < oldJb.getLocals().size())
			cmp = 2;
		else if (newJb.getLocals().size() > oldJb.getLocals().size())
			cmp = -2;
		else
			cmp = compareTypings(oldJb, newJb);

		G.v().out.println("cmp;" + jb.getMethod() + ";" + size + ";"
				+ oldTime + ";" + newTime + ";" + cmp);
	}

	private boolean typingFailed(JimpleBody b) {
		// Check to see if any locals are untyped
		{
			Iterator<Local> localIt = b.getLocals().iterator();

			while (localIt.hasNext()) {
				Local l = localIt.next();

				if (l.getType().equals(UnknownType.v())
						|| l.getType().equals(ErroneousType.v())) {
					return true;
				}
			}
		}

		return false;
	}

	/* Returns -1 if a < b, +1 if b < a, 0 if a = b and 3 otherwise. */
	private static int compareTypings(JimpleBody a, JimpleBody b) {
		int r = 0;

		Iterator<Local> ib = b.getLocals().iterator();
		for (Local v : a.getLocals()) {
			Type ta = v.getType(), tb = ib.next().getType();

			if (soot.jimple.toolkits.typing.fast.TypeResolver
					.typesEqual(ta, tb))
				continue;
			/*
			 * Sometimes there is no reason to choose between the char and byte /
			 * short types. Enabling this check allows one algorithm to select
			 * char and the other to select byte / short without returning
			 * incomparable.
			 */
			else if (true && ((ta instanceof CharType && (tb instanceof ByteType || tb instanceof ShortType))
				           || (tb instanceof CharType && (ta instanceof ByteType || ta instanceof ShortType))))
				continue;
			else if (soot.jimple.toolkits.typing.fast.AugHierarchy.ancestor_(
					ta, tb)) {
				if (r == -1)
					return 3;
				else
					r = 1;
			} else if (soot.jimple.toolkits.typing.fast.AugHierarchy.ancestor_(
					tb, ta)) {
				if (r == 1)
					return 3;
				else
					r = -1;
			} else
				return 3;
		}

		return r;
	}
}
