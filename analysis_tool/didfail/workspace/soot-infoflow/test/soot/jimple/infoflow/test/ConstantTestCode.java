/*******************************************************************************
 * Copyright (c) 2012 Secure Software Engineering Group at EC SPRIDE.
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the GNU Lesser Public License v2.1
 * which accompanies this distribution, and is available at
 * http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
 * 
 * Contributors: Christian Fritz, Steven Arzt, Siegfried Rasthofer, Eric
 * Bodden, and others.
 ******************************************************************************/
package soot.jimple.infoflow.test;

import soot.jimple.infoflow.test.android.ConnectionManager;
import soot.jimple.infoflow.test.android.TelephonyManager;

/**
 * tests constant tainting
 * @author Christian
 *
 */
public class ConstantTestCode {
	
	static final String tainted = TelephonyManager.getDeviceId();
	static final String[] staticArray = new String[1];
	final String[] fieldArray = new String[1];

	public void easyConstantFieldTest(){
		ConnectionManager cm = new ConnectionManager();
		cm.publish(tainted);
	}
	
	public void easyConstantVarTest(){
		final String e = TelephonyManager.getDeviceId();
		ConnectionManager cm = new ConnectionManager();
		cm.publish(e);
	}
	
	public void constantArrayTest(){
		String tainted =  TelephonyManager.getDeviceId();
		fieldArray[0] = tainted;
		
		ConnectionManager cm = new ConnectionManager();
		cm.publish(fieldArray[0]);
	}

	public void constantStaticArrayTest(){
		String tainted =  TelephonyManager.getDeviceId();
		staticArray[0] = tainted;
		
		ConnectionManager cm = new ConnectionManager();
		cm.publish(staticArray[0]);
	}

	public void constantFieldArrayTest(){
		String tainted =  TelephonyManager.getDeviceId();
		staticArray[0] = tainted;
		fieldArray[0] = tainted;
		
		ConnectionManager cm = new ConnectionManager();
		cm.publish(staticArray[0]);
		cm.publish(fieldArray[0]);
	}
	
	public void constantFieldTest(){
		ConstantClass c = new ConstantClass();
		ConnectionManager cm = new ConnectionManager();
		cm.publish(c.e);
	}
	
	class ConstantClass{
		final String e;
		public ConstantClass(){
			e = TelephonyManager.getDeviceId();
		}
	}

}
