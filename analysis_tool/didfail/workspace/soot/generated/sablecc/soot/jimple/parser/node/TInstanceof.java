/* This file was generated by SableCC (http://www.sablecc.org/). */

package soot.jimple.parser.node;

import soot.jimple.parser.analysis.*;

@SuppressWarnings("nls")
public final class TInstanceof extends Token
{
    public TInstanceof()
    {
        super.setText("instanceof");
    }

    public TInstanceof(int line, int pos)
    {
        super.setText("instanceof");
        setLine(line);
        setPos(pos);
    }

    @Override
    public Object clone()
    {
      return new TInstanceof(getLine(), getPos());
    }

    public void apply(Switch sw)
    {
        ((Analysis) sw).caseTInstanceof(this);
    }

    @Override
    public void setText(@SuppressWarnings("unused") String text)
    {
        throw new RuntimeException("Cannot change TInstanceof text.");
    }
}
