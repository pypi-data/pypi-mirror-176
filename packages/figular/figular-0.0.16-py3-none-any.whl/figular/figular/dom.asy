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

import "figular/style" as style;

struct dom {

  // We cannot use the primitive types here as it creates circular dependency
  // as primitives need to refer to dom also. So instead the dom methods are
  // called by the primitives who indicate their type by the method they call.
  // A real dom implementation can import this file and the primitives,
  // avoiding the circular dep and work with both.

  // Allow clients to notify us of next parent.
  void nextparentisatextbox();
  void nextparentisacircle();
  void nextparentisashape();
  void nextparentisaline();

  // Allow clients to notify us we need to add to the dom
  style addtextbox();
  style addcircle();
  style addshape();
  style addline();
}

// Global dom
dom dom;
