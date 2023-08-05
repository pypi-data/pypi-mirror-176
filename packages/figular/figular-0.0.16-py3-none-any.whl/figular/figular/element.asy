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

import "figular/primitives.asy" as primitives;

struct elementtype {
  private static int ind = 0;
  private int i;
  void operator init(int i) { this.i = i; }

  static elementtype textbox = elementtype(++ind);
  static elementtype circle = elementtype(++ind);
  static elementtype shape = elementtype(++ind);
  static elementtype line = elementtype(++ind);
}

string operator cast(elementtype et) {
  if(et == elementtype.textbox) { return "textbox"; }
  if(et == elementtype.circle) { return "circle"; }
  if(et == elementtype.shape) { return "shape"; }
  if(et == elementtype.line) { return "line"; }
  return "unknown";
}

struct element {
  elementtype et;
  textbox t;
  circle c;
  shape s;
  line l;

  void operator init(textbox t) {
    this.t = t;
    this.et = elementtype.textbox;
  }

  void operator init(circle c) {
    this.c = c;
    this.et = elementtype.circle;
  }

  void operator init(shape s) {
    this.s = s;
    this.et = elementtype.shape;
  }

  void operator init(line l) {
    this.l = l;
    this.et = elementtype.line;
  }

}

bool operator ==(element p1, element p2) {
  // Uninitialised structs will never be equal
  return (p2.et == p1.et && 
          (p2.t == p1.t || p2.c == p1.c || p2.s == p1.s || p2.l == p1.l));
}

bool operator !=(element p1, element p2) {
  return !(p1 == p2);
}
