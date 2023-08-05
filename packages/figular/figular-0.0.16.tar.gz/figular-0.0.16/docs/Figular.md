<!--
SPDX-FileCopyrightText: 2021-2 Galagic Limited, et al. <https://galagic.com>

SPDX-License-Identifier: CC-BY-SA-4.0

figular generates visualisations from flexible, reusable parts

For full copyright information see the AUTHORS file at the top-level
directory of this distribution or at
[AUTHORS](https://gitlab.com/thegalagic/figular/AUTHORS.md)

This work is licensed under the Creative Commons Attribution 4.0 International
License. You should have received a copy of the license along with this work.
If not, visit http://creativecommons.org/licenses/by/4.0/ or send a letter to
Creative Commons, PO Box 1866, Mountain View, CA 94042, USA.
-->

# Figular

Figular lets you build visualisations. You can choose from a range of
existing figures that can be customised or build your own (in future).

## Table of Contents

* [Figures](#figures)
* [Custom Figures](#custom-figures)
* [Styling](#styling)
  * [Applying Style](#applying-style)
  * [Style Elements](#style-elements)
    * [Circle](#circle)
    * [Shape](#shape)
    * [Line](#line)
    * [Text Box](#text-box)
  * [Style Properties](#style-properties)
    * [Border Style](#border-style)
    * [Colors](#colors)
    * [Font Families](#font-families)
* [Threat Model](#threat-model)

## Figures

A figure is a self-contained visualisation that can adjust itself based on your
content. Content can be parameters that control style (rotation, layout) and
data that populates the figure (text, images). Figular comes with a range of our
own figures, documentation on each of them is linked below:

* [Concept/circle](figures/concept/circle.md)
* [Org/orgchart](figures/org/orgchart.md)

Please help us grow this list by contributing to the project. You can develop
your own custom figures too, for more on this see [custom
figures](#custom-figures) below.

Figures can come from different repositories. If no repository is specified the
default is 'Figular' which is what comes bundled as standard with any
installation. At present we do not support repositories so this is purely
theoretical. Our inspiration comes from [flatpak](https://flatpak.org/).

Each figure has a unique, case-insensitive name within its repository. Related
figures are grouped together in a tree-like structure. Levels in the tree are
separated by a forward slash `/`, e.g.  'concept/circle'. Our inspiration comes
from URLs.

Figures can be versioned, if a version is not supplied the latest is assumed.
The version is not part of the name however. Versioning is inspired by [Semantic
Versioning](https://semver.org/). New versions should not break older usage
without a major version bump for example.

In future we may also support metadata such as categories/tags and other
information. Inspiration comes from [PyPi](pypi.org/).

## Custom Figures

Note: this section does not yet show all the ways you can create your own
figures but does provide an example to get you started. To understand what's
possible you'll have to inspect the source code for now.

To develop your own figures you can provide custom Asymptote code to the `fig`
command:

```bash
fig mycode.asy DATA [STYLE]
```

Figular will expect your code to provide a `run` method we will call into:

```asymptote
void run(picture pic, string[] input) {
  ...
}
```

Any DATA provided on the cmdline will be available through the `input` argument,
split by lines. If DATA is not provided it will be taken from stdin. Any styling
will have already been setup as rules on our styledom. To take advantage just
use our drawing primitives and they will be styled accordingly. For example if
you create a file `myfile.asy` with this content:

```asymptote
import "figular/primitives" as primitives;

void run(picture pic, string[] input) {
  real radius = 20;
  page p = page(pic);

  for(int i = 0 ; i < input.length ; ++i) {
    pair pos = (i*radius*3, 0);
    circle c = circle(p, radius, pos);
    textbox(p, 2*radius, pos, input[i], c=c);
  }
  p.print();
}
```

You could then use it below supplying data and styling just like we do with the
build-in figures:

```bash
fig myfile.asy $'Hello\nThere' '{ "circle":{ "background_color": "pink" } }'
```

## Styling

Various parts of a figure can be styled. On the website style is changed through
forms on the Figure's page. Consult the [figure](#figures) pages above for help
with the website.

At the cmdline and API style can be supplied as an argument in the form of a
JSON document. For example for the concept/circle figure you can apply settings
like this:

```json
{
  "figure_concept_circle": {
    "rotation": 30,
    "middle": true,
  }
}
```

At the cmdline a full example looks like this:

```bash
fig concept/circle $'Hello\nThere' '{ "figure_concept_circle": { "rotation": 30 }}'
```

See the individual figure pages [above](#figures) for more information on what
can be applied to each figure and more cmdline examples.

Further to this each figure uses basic elements to compose itself like
circles, shapes, textboxes, lines. These can all be styled too. The full details
on each of them are below, e.g. [circle](#circle). However next we'll
look at how to choose where we apply style.

### Applying Style

Figular uses a basic kind of [CSS](https://en.wikipedia.org/wiki/CSS) that we've
mangled into a JSON doc. You can apply style in three ways:

* Select an element type no matter where it appears in the Figure. This is
  equivalent to a CSS rule like "p" that targets all paragraphs. Just include
  the element's style JSON object at the top-level of the document. For example,
  to style all textboxes:

  ```JSON
  {
    "textbox": {
      "background_color": "blue",
      "border_color": "pink",
    }
  }
  ```

* Selecting an element type depending on its place in the hierarchy - similar to
  CSS' [child
  combinator](https://developer.mozilla.org/en-US/docs/Learn/CSS/Building_blocks/Selectors/Combinators#child_combinator)
  ">".

  For example to style any textbox that is the child of a circle, (equivalent to
  a "circle > textbox" rule in CSS) we put a textbox object inside a circle
  object:

  ```JSON
  {
    "circle": {
      "textbox": {
        "color": "blue",
        "font_size": 24
      }
    }
  }
  ```

  We can repeat this nesting of elements to any depth.

* Selecting a specific child of a parent - similar to CSS' pseudo-class
  [:nth-child()](https://developer.mozilla.org/en-US/docs/Web/CSS/:nth-child).

  Currently this only works for textboxes that are inside shapes (equivalent to
  CSS "shape > textbox:nth-child(2)") and only up to the 3rd child - but it will
  be extended to everything eventually.

  For example to target the 2nd child textbox inside a shape:

  ```JSON
    "shape": {
      "textbox_nth_child_2": {
        "color": "blue",
        "font_size": 24
      }
  ```

Keep reading to see all the properties for each of the primitive elements.

### Style Elements

#### Circle

First a full example of the JSON that can be used to style circles:

```json
{
  "circle": {
    "background_color": "blue",
    "border_color": "pink",
    "border_width": 2,
    "border_style": "dashed"
  }
}
```

At the cmdline this might look like:

```bash
fig concept/circle $'Hello\nThere' \
    '{ "circle": { "background_color": "blue",
                   "border_color": "pink",
                   "border_width": 2,
                   "border_style": "dashed"
     } }'
```

Each parameter is optional. Here's a description of them all:

|Name|Type|Default|Description|
|----|----|-------|-----------|
|background_color|Color (see Colors below)|Off-black, specifically 'heavygray', 25% gray or `#404040`|Background color, equivalent to CSS' property [background-color](https://developer.mozilla.org/en-US/docs/Web/CSS/background-color).
|border_color|Color (see Colors below)|Black|Border color, equivalent to CSS' property [border-color](https://developer.mozilla.org/en-US/docs/Web/CSS/border-color).
|border_width|Float, 0-100|0|Border width in PostScript big points (1/72 of an inch). Equivalent to CSS' property [border-width](https://developer.mozilla.org/en-US/docs/Web/CSS/border-width).
|border_style|Enumeration|Solid|Style of the border. Possible values: "solid, dotted, dashed, longdashed, dashdotted, longdashdotted" Equivalent to CSS' property [border-style](https://developer.mozilla.org/en-US/docs/Web/CSS/border-style).

#### Shape

Shapes are used by Figures for any filled path that is not better served by a
circle. First a full example of the JSON that can be used to style shapes:

```json
{
  "shape": {
    "background_color": "blue",
    "border_color": "pink",
    "border_width": 2,
    "border_style": "dashed"
  }
}
```

At the cmdline this might look like:

```bash
fig org/orgchart "$(cat << EOF
The Great Company
Managing Director|Managing the direction|The Great Company
EOF
)" $'{ "shape": { "background_color": "blue",
                 "border_color": "pink",
                 "border_width": 2,
                 "border_style": "dashed"
   } }'
```

Each parameter is optional. Here's a description of them all:

|Name|Type|Default|Description|
|----|----|-------|-----------|
|background_color|Color (see Colors below)|Off-black, specifically 'heavygray', 25% gray or `#404040`|Background color, equivalent to CSS' property [background-color](https://developer.mozilla.org/en-US/docs/Web/CSS/background-color).
|border_color|Color (see Colors below)|Black|Border color, equivalent to CSS' property [border-color](https://developer.mozilla.org/en-US/docs/Web/CSS/border-color).
|border_width|Float, 0-100|0|Border width in PostScript big points (1/72 of an inch). Equivalent to CSS' property [border-width](https://developer.mozilla.org/en-US/docs/Web/CSS/border-width).
|border_style|Enumeration|Solid|Style of the border. Possible values: "solid, dotted, dashed, longdashed, dashdotted, longdashdotted" Equivalent to CSS' property [border-style](https://developer.mozilla.org/en-US/docs/Web/CSS/border-style).

#### Line

Lines are used by Figures for any unfilled path. First a full example of the
JSON that can be used to style lines:

```json
{
  "line": {
    "border_color": "pink",
    "border_width": 2,
    "border_style": "dashed"
  }
}
```

At the cmdline this might look like:

```bash
fig org/orgchart "$(cat << EOF
The Great Company
Managing Director|Managing the direction|The Great Company
EOF
)" $'{ "line": {
    "border_color": "pink",
    "border_width": 2,
    "border_style": "dashed"
   } }'
```

Each parameter is optional. Here's a description of them all:

|Name|Type|Default|Description|
|----|----|-------|-----------|
|border_color|Color (see Colors below)|Black|Border color, equivalent to CSS' property [border-color](https://developer.mozilla.org/en-US/docs/Web/CSS/border-color).
|border_width|Float, 0-100|0|Border width in PostScript big points (1/72 of an inch). Equivalent to CSS' property [border-width](https://developer.mozilla.org/en-US/docs/Web/CSS/border-width).
|border_style|Enumeration|Solid|Style of the border. Possible values: "solid, dotted, dashed, longdashed, dashdotted, longdashdotted" Equivalent to CSS' property [border-style](https://developer.mozilla.org/en-US/docs/Web/CSS/border-style).

#### Text Box

First a full example of the JSON that can be used to style text boxes:

```json
{
  "textbox": {
    "color": "pink",
    "font_family": "Helvetica",
    "font_size": 16
  }
}
```

At the cmdline this might look like:

```bash
fig concept/circle $'Hello\nThere' \
    '{ "textbox": {
      "color": "pink",
      "font_family": "Helvetica",
      "font_size": 16
      } }'
```

Each parameter is optional. Here's a description of them all:

|Name|Type|Default|Description|
|----|----|-------|-----------|
|color|Color (see Colors below)|Off-white, specifically `lightgray`, 90% gray or `#E6E6E6`|Foreground color, equivalent to CSS' property [color](https://developer.mozilla.org/en-US/docs/Web/CSS/color).
|font_family|Font (see Fonts below)|Computer Modern Roman|Font family, equivalent to CSS' property [font-family](https://developer.mozilla.org/en-US/docs/Web/CSS/font-family).
|font_size|Float, 0-300|12pt|Font size in points (1pt = 1/72.27 inches), equivalent to CSS' property [font-size](https://developer.mozilla.org/en-US/docs/Web/CSS/font-size).

### Style Properties

#### Border Style

Choose from the following settings:

* solid
* dotted
* dashed
* longdashed
* dashdotted
* longdashdotted

#### Colors

Color names are predefined:

* Black
* Cyan
* Magenta
* Yellow
* black
* blue
* brown
* chartreuse
* cyan
* darkblue
* darkbrown
* darkcyan
* darkgray
* darkgreen
* darkgrey
* darkmagenta
* darkolive
* darkred
* deepblue
* deepcyan
* deepgray
* deepgreen
* deepgrey
* deepmagenta
* deepred
* deepyellow
* fuchsia
* gray
* green
* grey
* heavyblue
* heavycyan
* heavygray
* heavygreen
* heavygrey
* heavymagenta
* heavyred
* lightblue
* lightcyan
* lightgray
* lightgreen
* lightgrey
* lightmagenta
* lightolive
* lightred
* lightyellow
* magenta
* mediumblue
* mediumcyan
* mediumgray
* mediumgreen
* mediumgrey
* mediummagenta
* mediumred
* mediumyellow
* olive
* orange
* paleblue
* palecyan
* palegray
* palegreen
* palegrey
* palemagenta
* palered
* paleyellow
* pink
* purple
* red
* royalblue
* salmon
* springgreen
* white
* yellow

#### Font Family

Font family names are predefined:

* Avant Garde
* Bookman
* Computer Modern Roman
* Computer Modern Sans
* Computer Modern Teletype
* Courier
* DejaVu Sans
* Helvetica
* New Century Schoolbook
* Palatino
* Symbol
* Times New Roman
* Zapf Chancery
* Zapf Dingbats

## Threat Model

Figular tries to guarantee the following:

* There is no input that can cause Figular to do anything other than render an
  image.
* Figular will always return a timely result - whether an image can be produced
  or rendering was aborted.
* Figular will not reveal information about the system it is run on in its
  output.

Assumptions:

* The host system is trusted. For Figular cmdline we do not control the host
  system. For SaaS we do and should ensure the system is trusted.

* The user has an authentic copy of Figular. We should ensure all distribution
  channels provide a means by which the user can verify they have received an
  authentic copy. Further we should ensure our channels cannot be hijacked i.e.
  secure supply chain.

  Current distribution channels for Figular include:

  * [GitLab](gitlab.com/)
  * [PyPi](https://pypi.org/)

The adversary's attacks will vary depending on usage as detailed below.

### Figular at the Cmdline

The adversary's only means of attacking others is by communicating suggested
malicious input/usage to a target user i.e. social engineering. Attacks include:

* Exploitation of user system: adversary gains access to run arbitrary code as
  user on target system.
* Denial of service: excessive use of system resources
* If the adversary can gain access to a user's results then further attack
  vectors are possible. The user would have to play along with attacker by
  posting results back to adversary so further social engineering is required:
  * Adversary wishes to hijack compute power for own purposes by suggesting
    malicious input that causes some desirable computation to be performed and
    result to be contained in Figular output.
  * Adversary to reveal sensitive information about user/target system through
    Figular output, e.g. credentials, file contents, IP address, digital
    currency wallet.

### Figular SaaS

Attacks include:

* Exploitation of Figular infrastructure: adversary uses our compute power for
  their own purpose.
* Denial of service to others: excessive use of system resources.
* Information theft: mining of information from Figular infrastructure such as
  credentials, certificates in order to perpetrate further attacks e.g.
  supply chain attack, impersonation.
* Theft of users' data, renderings, etc by exploiting side-channels,
  escalation of privilege, code exploits etc.
  * One vector is to attack the current use of the `/tmp` filesystem for
    intermediate results of the render. If there was some naming collision or other
    method of tricking the request into reading from the wrong dir then
    results could be delivered to the wrong user.

    To mitigate we create a unique temp dir per request that is cleaned up after
    use. Inside this we also use a temp filename for the final output.
    Intermediate files that Asymptote creates are based on the final output
    filename so should also be using the same temp filename stem.
* Impersonation of other users to gain access to their data.
