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

import "figular/selector" as selector;

struct domnode {
  element e;
  selectorlist s; // is it the complete path?
  domnode[] children;

  void operator init(element e, selectorlist s) {
    this.e = e;
    this.s = s;
  }
}

struct domtree {
  private domnode[] nodes;
  private element[] parent;

  private void nextparent(element el) {
    if(this.parent.length !=0) {
      abort("domtree: another parent was added before the last one had its child put in the tree");
    }
    this.parent.push(el);
  }

  private domnode findparent(domnode[] nodes, element parent) {
    domnode result = null;
    for(var n: nodes) {
      if(n.e != parent) {
        result = findparent(n.children, parent);
        if (result != null) {
          break;
        }
      } else {
        result = n;
        break;
      }
    }
    return result;
  }

  private selectorlist addtoparentintree(element e) {
    element parent = this.parent.pop();

    domnode treeparent = findparent(this.nodes, parent);

    if(treeparent == null) {
      abort("domtree: we never found the parent");
    }

    selectorlist sl = selectorlist(treeparent.s,
                                   selector(e.et, treeparent.children.length+1));
    domnode dn = domnode(e, sl);
    treeparent.children.push(dn);
    return sl;
  }

  private selectorlist addtotree(element e) {
    selectorlist result;
    if(this.parent.length > 0) {
      result = addtoparentintree(e);
    } else {
      selectorlist sl = selectorlist(selector(e.et, nodes.length+1));
      domnode dn = domnode(e, sl);
      nodes.push(dn);
      result = sl;
    }
    return result;
  }

  private element elementoflasttextbox() {
    return element(textbox.lasttextbox);
  }

  private element elementoflastcircle() {
    return element(circle.lastcircle);
  }

  private element elementoflastshape() {
    return element(shape.lastshape);
  }

  private element elementoflastline() {
    return element(line.lastline);
  }

  selectorlist addtextbox() {
    return addtotree(elementoflasttextbox());
  }

  selectorlist addcircle() {
    return addtotree(elementoflastcircle());
  }

  selectorlist addshape() {
    return addtotree(elementoflastshape());
  }

  selectorlist addline() {
    return addtotree(elementoflastline());
  }

  void nextparentisatextbox() {
    this.nextparent(element(textbox.lastparent));
  }

  void nextparentisacircle() {
    this.nextparent(element(circle.lastparent));
  }

  void nextparentisashape() {
    this.nextparent(element(shape.lastparent));
  }

  void nextparentisaline() {
    this.nextparent(element(line.lastparent));
  }
}
