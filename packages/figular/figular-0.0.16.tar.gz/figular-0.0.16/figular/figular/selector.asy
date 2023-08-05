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

import "figular/element" as element;

// Important for now selectors are immutable as they may be shared when we
// create new selectorlists based on other selectorlists below.

struct selector {
  private bool haselement;
  private elementtype et;
  private bool hasindex;
  private int index;

  // Has to be one or the other or both
  void operator init(elementtype et) {
    haselement = true;
    hasindex = false;
    this.et = et;
  }
  void operator init(int index) {
    haselement = false;
    hasindex = true;
    this.index = index;
  }
  void operator init(elementtype et, int index) {
    haselement = true;
    hasindex = true;
    this.et = et;
    this.index = index;
  }

  bool haselement() {
    return this.haselement;
  }

  bool hasindex() {
    return this.hasindex;
  }

  bool match(selector s) {
    bool result = false;
    if(this.haselement && s.haselement) {
      if(this.et == s.et) {
        result = true;
      } else {
        return false;
      }
    } 
    if(this.hasindex && s.hasindex) {
      if(this.index == s.index) {
        result = true;
      } else {
        return false;
      }
    }

    return result;
  }

  string tostring() {
    string result;

    if(this.haselement) {
      result += "element: " + this.et + " ";
    }
    if(this.hasindex) {
      result += "index: " + (string)this.index + " ";
    }
    return "{ " + result + "}";
  }
}

string operator cast(selector s) {
  return s.tostring();
}

struct selectorlist {
  selector[] selectors;

  void operator init(...selector[] selectors) {
    this.selectors = selectors;
  }

  void operator init(selectorlist s, selector a) {
    // This requires selectors to be immutable
    this.selectors = copy(s.selectors);
    this.selectors.push(a);
  }

  bool isselectedby(selectorlist sl) {
    // If it's longer we can't match
    if(sl.selectors.length > this.selectors.length) { return false; }

    // Special case if it's length 1 and has an element it's
    // a universal matcher so compare to end of my path
    if(sl.selectors.length == 1 && sl.selectors[0].haselement()) {
      return selectors[selectors.length-1].match(sl.selectors[0]);
    }

    for(var i=0; i<selectors.length ; ++i) {
      if(i >= sl.selectors.length) {
        // If we've exhausted sl, the last piece included an index and our path
        // is not exhausted then it hasn't matched. i.e. nthchild(2) should not match
        // all the things under the second node in the tree.
        if(sl.selectors[i-1].hasindex() && i < this.selectors.length) {
          return false;
        }

        return true;
      }
      if(!selectors[i].match(sl.selectors[i])) {
        return false;
      }
    }
    return true;
  }

  string tostring() {
    string result;
    for(var s: this.selectors) {
      result += s;
    }
    return result;
  }
}

string operator cast(selectorlist sl) {
  return sl.tostring();
}
