// SPDX-FileCopyrightText: 2021-2 Galagic Limited, et al. <https://galagic.com>
//
// SPDX-License-Identifier: AGPL-3.0-or-later
//
// figular generates visualisations from flexible, reusable parts
//
// For full copyright information see the AUTHORS file at the top-level
// directory of this distribution or at
// [AUTHORS](https://gitlab.com/thegalagic/figular/AUTHORS.md)
//
// This program is free software: you can redistribute it and/or modify it under
// the terms of the GNU Affero General Public License as published by the Free
// Software Foundation, either version 3 of the License, or (at your option) any
// later version.
//
// This program is distributed in the hope that it will be useful, but WITHOUT
// ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
// FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more
// details.
//
// You should have received a copy of the GNU Affero General Public License
// along with this program. If not, see <https://www.gnu.org/licenses/>.

import "figular/page.asy" as page;

// We adopt asy's defaults to make use of their addition operator below
pen nullpen = defaultpen;

struct style {
  pen border_color;
  pen strokeopacity;
  real border_width;
  pen border_style;
  pen join;
  pen cap;
  pen background_color;
  pen font_family;
  pen color;
  real font_size;

  private pen flattenlinestyle() {
    // This only works as we use asy's defaults as our defaults and the
    // addition operator make sure all other non-default attributes of the
    // rightmost pen will override those of the leftmost pen.
    pen result=defaultpen;
    if(this.border_color != nullpen) {
      // Strip out our colour first as otherwise asy will add the colours
      result = colorless(result) + border_color;
    }
    if(this.strokeopacity != nullpen) {
      result += this.strokeopacity;
    }
    if(this.border_width != realMax) {
      result += this.border_width;
    }
    if(this.border_style != nullpen) {
      result += this.border_style;
    }
    if(this.join != nullpen) {
      result += this.join;
    }
    if(this.cap != nullpen) {
      result += this.cap;
    }
    return result;
  }

  private pen flattentextstyle() {
    pen result=colorless(this.font_family) + this.color;
    if(this.font_size != realMax) {
      result += fontsize(this.font_size);
    }
    return result;
  }

  void operator init(pen border_color=nullpen,
                     pen strokeopacity=nullpen,
                     real border_width=realMax,
                     pen border_style=nullpen,
                     pen join=nullpen,
                     pen cap=nullpen,
                     pen background_color=nullpen,
                     pen font_family=nullpen,
                     pen color=nullpen,
                     real font_size=realMax) {
    this.border_color=border_color;
    this.strokeopacity=strokeopacity;
    this.border_width=border_width;
    this.border_style=border_style;
    this.join=join;
    this.cap=cap;
    this.background_color=background_color;
    this.font_family=font_family;
    this.color=color;
    this.font_size=font_size;
  }

  drawnpath draw(page p, path g) {
    pen finallinestyle = flattenlinestyle();
    drawnpath dp = drawnpath(g, new void(picture p) { draw(p, g, finallinestyle); });
    p.push(dp);
    return dp;
  }

  drawnpath filldraw(page p, path g) {
    pen finallinestyle = flattenlinestyle();
    drawnpath dp;

    // Asymptote's filldraw and draw seem to always draw an outline even when
    // linewidth=0. Bug?
    if(linewidth(finallinestyle) > 0) {
      dp = drawnpath(g, new void(picture p) { filldraw(p, g, this.background_color, finallinestyle); });
    } else {
      dp = drawnpath(g, new void(picture p) { fill(p, g, this.background_color); });
    }
    p.push(dp);
    return dp;
  }

  Label textframe(page p, pair place, align align, string text) {
    pen finaltextstyle = flattentextstyle();
    Label l = Label(text, place, align, finaltextstyle);
    p.push(l);
    return l;
  }
}

style operator+(style a, style b) {
  style result;
  if(b.border_color != nullpen) {
    // Strip out our colour first as otherwise asy will add the colours
    result.border_color = b.border_color;
  } else {
    result.border_color = a.border_color;
  }
  if(b.strokeopacity != nullpen) {
    result.strokeopacity = b.strokeopacity;
  } else {
    result.strokeopacity = a.strokeopacity;
  }
  if(b.border_width != realMax) {
    result.border_width = b.border_width;
  } else {
    result.border_width = a.border_width;
  }
  if(b.border_style != nullpen) {
    result.border_style = b.border_style;
  } else {
    result.border_style = a.border_style;
  }
  if(b.join != nullpen) {
    result.join = b.join;
  } else {
    result.join= a.join;
  }
  if(b.cap != nullpen) {
    result.cap = b.cap;
  } else {
    result.cap= a.cap;
  }
  if(b.background_color != nullpen) {
    result.background_color = b.background_color;
  } else {
    result.background_color= a.background_color;
  }
  if(b.font_family != nullpen) {
    result.font_family = b.font_family;
  } else {
    result.font_family = a.font_family;
  }
  if(b.color != nullpen) {
    result.color = b.color;
  } else {
    result.color= a.color;
  }
  if(b.font_size != realMax) {
    result.font_size = b.font_size;
  } else {
    result.font_size = a.font_size;
  }
  return result;
}

style nullstyle = style();

// ----------------------------------------------------------------------------
// Fonts
// ----------------------------------------------------------------------------

// To access system fonts - see asymptote_doc
usepackage("fontspec");

pen getfont(string fontname, string series="m") {
  return fontcommand("\setmainfont{"+fontname+
                     "}\fontseries{"+series+
                     "}\selectfont");
}

struct fontrec {
  pen wield;
  string family;
  string style;

  void operator init(pen wield, string family, string style) {
    this.wield = wield;
    this.family = family;
    this.style = style;
  }
}

struct fontinfo {
  // TODO:
  // * We desperately need a uniform way of categorising/referring to typefaces/fonts
  // * Some fonts such as the built-in helpers for standard PostScript fonts end up being
  //   substituted in final PDF. Should it not be the case that you get what
  //   you request or should it work like the web and substitute as/when
  //   needed.     
  fontrec[] all;
  fontrec avantgarde = all.push(fontrec(AvantGarde(), "Avant Garde", "Normal"));
  fontrec avantgarde_bold = all.push(fontrec(AvantGarde("b"), "Avant Garde", "Bold"));
  fontrec bookman = all.push(fontrec(Bookman(), "Bookman", "Normal"));
  fontrec bookman_bold = all.push(fontrec(Bookman("b"), "Bookman", "Bold"));
  fontrec computermodern_roman = all.push(fontrec(font("OT1", "cmr", "m", "n"), "Computer Modern Roman", "Normal"));
  fontrec computermodern_roman_bold = all.push(fontrec(font("OT1", "cmr", "b", "n"), "Computer Modern Roman", "Bold"));
  fontrec computermodern_sansserif = all.push(fontrec(font("OT1", "cmss", "m", "n"), "Computer Modern Sans Serif", "Normal"));
  fontrec computermodern_sansserif_bold = all.push(fontrec(font("OT1", "cmss", "b", "n"), "Computer Modern Sans Serif", "Bold"));
  fontrec computermodern_teletype = all.push(fontrec(font("OT1", "cmtt", "m", "n"), "Computer Modern Teletype", "Normal"));
  // There is no bold cmtt, it falls back to plain cmtt. We need to decide how
  // we'll deal with fonts that don't support all possible stylings.
  fontrec computermodern_teletype_bold = all.push(fontrec(font("OT1", "cmtt", "b", "n"), "Computer Modern Teletype", "Bold"));
  fontrec courier = all.push(fontrec(Courier(), "Courier", "Normal"));
  fontrec courier_bold = all.push(fontrec(Courier("b"), "Courier", "Bold"));
  fontrec dejavu_sansserif = all.push(fontrec(getfont("DejaVu Sans"), "DeJaVu Sans Serif", "Normal"));
  fontrec dejavu_sansserif_bold = all.push(fontrec(getfont("DejaVu Sans", "b"), "DeJaVu Sans Serif", "Bold"));
  fontrec helvetica = all.push(fontrec(Helvetica(), "Helvetica", "Normal"));
  fontrec helvetica_bold = all.push(fontrec(Helvetica("b"), "Helvetica", "Bold"));
  fontrec newcenturyschoolbook = all.push(fontrec(NewCenturySchoolBook(), "New Century Schoolbook", "Normal"));
  fontrec newcenturyschoolbook_bold = all.push(fontrec(NewCenturySchoolBook("b"), "New Century Schoolbook", "Bold"));
  fontrec palatino = all.push(fontrec(Palatino(), "Palatino", "Normal"));
  fontrec palatino_bold = all.push(fontrec(Palatino("b"), "Palatino", "Bold"));
  fontrec symbol = all.push(fontrec(Symbol(), "Symbol", "Normal"));
  fontrec symbol_bold = all.push(fontrec(Symbol("b"), "Symbol", "Bold"));
  fontrec timesroman = all.push(fontrec(TimesRoman(), "Times Roman", "Normal"));
  fontrec timesroman_bold = all.push(fontrec(TimesRoman("b"), "Times Roman", "Bold"));
  fontrec zapfchancery = all.push(fontrec(ZapfChancery(), "Zapf Chancery", "Normal"));
  fontrec zapfchancery_bold = all.push(fontrec(ZapfChancery("b"), "Zapf Chancery", "Bold"));
  fontrec zapfdingbats = all.push(fontrec(ZapfDingbats(), "Zapf Dingbats", "Normal"));
  fontrec zapfdingbats_bold = all.push(fontrec(ZapfDingbats("b"), "Zapf Dingbats", "Bold"));
}

fontinfo font;

pen operator cast(fontrec fs) { return fs.wield; };
