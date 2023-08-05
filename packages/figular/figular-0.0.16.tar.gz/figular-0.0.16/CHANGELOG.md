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

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project will adhere to [Semantic
Versioning](https://semver.org/spec/v2.0.0.html) once we hit a 1.X release.

## [Unreleased]

## [0.0.16 - 2022-11-10](https://gitlab.com/thegalagic/figular/-/releases/v0.0.16)

### Changed

* The JS and HTML for our Figures has been consolidated into a single source
  file for each. This will allow us to add many more figures without high
  duplication. Also added simple testing of our HTML against what's expected.
  This ensures we can develop safely and break figures less easily.
  Downstream Hugo sites must change to the 'figular' widget and supply a few
  more params, see SelfHosting docs.
* The development environment is now assumed to be a toolbx container. This
  allows us to set the versions of Asymptote and Hugo for repeatable tests. Our
  existing dockerfile test is now converted to run on the host with
  flatpak-spawn.

## [0.0.15 - 2022-10-12](https://gitlab.com/thegalagic/figular/-/releases/v0.0.15)

### Added

* Internal
  * eslint added for linting the JavaScript. All linting problems squashed.
  * Asymptote 2.832 - some non-cosmetic changes to expected test results.

### Fixed

* Our hugo module's declared dependency on Wowchemy was no longer correct, they have
  renamed their repo. On further thought we've removed the dependency altogether
  so downstream has complete flexibility over whether to use Wowchemy or a fork.
  This solves `hugo mod` issues downstream where the dep could not be found:

  ```text
  go: module github.com/wowchemy/wowchemy-hugo-modules@upgrade found
  (v4.8.0+incompatible), but does not contain package
  github.com/wowchemy/wowchemy-hugo-modules/wowchemy/v5
  ```

## [0.0.14 - 2022-10-07](https://gitlab.com/thegalagic/figular/-/releases/v0.0.14)

### Added

* Website: administrators can now control the timeout for Figure requests from
  the backend, by default it's 10s. Details are in the docs: [SelfHosting](docs/SelfHosting.md)

## [0.0.13 - 2022-09-30](https://gitlab.com/thegalagic/figular/-/releases/v0.0.13)

### Fixed

* Website: download button too close vertically to Figures, added some space.
  Also fixed layout on narrow screens where the download button would jump to
  left side and the format buttons would span whole screen.

## [0.0.12 - 2022-09-30](https://gitlab.com/thegalagic/figular/-/releases/v0.0.12)

### Fixed

* Website: set the right mime type and download filename when user switches
  output format. This was particular issue on FF for Android where SVGs where
  saved as PNGs and thus not usable. Also simplified Figure JavaScript, use
  blobs for both SVG and PNG formats. This has no effect on user experience.
* Website: Hugo Figure widgets: remove `not_ready` parameter, which was for use before
  the backend was ready.

## [0.0.11 - 2022-09-29](https://gitlab.com/thegalagic/figular/-/releases/v0.0.11)

### Added

* Support for PNG output from the API and website so users can download in
  format they choose. Webpges default to PNG now as it's got wider support than
  SVG on base OS's e.g. Windows. Breaking change to API.
* Small extra test on our asy cleanse code, no meaningful change though.

### Changed

* Website: better file names for downloads - based on the example media's name
  from the widget page. So downloading the circle figure gives a file called
  'circle.png'.
* Use a StreamingResponse in the API as suggested by FastAPI for serving
  performant media
* Detect the state where Asy produced no files and give user a 422 status code
  with a custom msg. This can occur where user has entered meaningless
  whitespace.
* Our API testing now uses the FastAPI testclient which is much more sane then
  calling path methods directly.

### Fixed

* Orgchart bug fixed where it produced empty graphic even with no valid data

## [0.0.10 - 2022-09-27](https://gitlab.com/thegalagic/figular/-/releases/v0.0.10)

### Added

* Styling: large change to introduce a DOM that understands hierarchy and
  replace existing flat one. This allows us to style everything in the Figures
  we have so far. It supports both:

  * finding the 'nth-child' of a parent, e.g. `shape > textbox_nth_child_1`
  * child combinators (CSS' ">"), e.g. `shape > textbox`

  It will give primitives the correct style based on any rules that have been
  added. Child combinators allow us to reach anything and nth-child let's us
  target a specific primitive in a drawing rather than all of given type.
* On the website you can now style the orgchart. The user can choose a wide
  layout, tighter spacing on lower layers and control horiz/vert spacing. There
  are also controls for styling the shapes which are used to draw each role's
  card and the two textboxes that are for the title and subtitle.
* For fonts you can now style their 'weight', with normal and bold options for
  now. Note "Computer Modern Teletype" has no bold face and falls back to
  normal, but all the rest have a bold alternative. This is available on the
  website, cmdline and API.

### Changed

* API/cmdline updated to allow styling with the new dom. Note we have not yet
  exposed all the possible styling combinations, just a restricted set for the
  figures we have so far. Breaking change.
* Figures were updated to set their style with the new dom and draw their
  primitives in the dom's hierarchy so elements have a logical relationship
  (text boxes are underneath the shapes they are drawn inside). Circle's styling
  has changed slightly, textbox is now separate.
* API: orgchart now takes our standard Message which means it is also much more
  stylable. This is a breaking change.
* Internal changes:
  * Some stray asy 'include's where switched to imports. Include should not be
    needed.
  * Aligned asy style's members with CSS names

### Fixed

* Asy: circle and shape's styles were intermixed in stylesheet, now separated.

## [0.0.9 - 2022-09-05](https://gitlab.com/thegalagic/figular/-/releases/v0.0.9)

### Added

* In the website you can style the circles from which the Circle Figure is drawn
  with new settings: background-color, color, border-color, border-width,
  border-style, border-size, font-family, font-size. These are all available as
  new input forms. Also style has been broken up into collapsible sections as
  the page is growing vertically.

### Changed

* Docs updated to show all the new styling available on the Circle Figure in
  screenshots and all examples. Some of the previous cmdline example should have
  already been updated as the API changed before.
* Figular stylesheet: the default colors have been changed to
  ones which are named in Asymptote. The dark gray has actually had to change
  shade as Asy had no name for 20% gray, we use 'heavygray' which is 25% gray as
  closest. This was required as our web color dropdown only allows named colors
  right now.

## [0.0.8 - 2022-08-25](https://gitlab.com/thegalagic/figular/-/releases/v0.0.8)

### Fixed

* We were not logging stderr when encoutering failures in the API.
* Cmdline: return a non-zero return code on errors.

### Added

* We now test the Dockerfile and API by spining up a container. This helps
  detect any misconfigurations in the runtime environment.
* Cmdline and API: for the circle Figure you can now style the 'circle'
  primitive it is drawn with, controlling background-color, border-color etc.
* Website: for the circle Figure there is now a much greater choice of fonts.

### Changed

* More generous limits on Figure data - increased from 1k to 5k characters.
* The cmdline has changed, now we expect args DATA and optional STYLE as a JSON
  doc. Initially we can only style circle but we'll extend this in future. This
  also means our pip install requires pydantic as a dependancy. Circle also no
  longer needs `blob=`. Docs have been updated.
* The API for circle has changed as we move towards a simpler message containing
  just 'data' and 'style' for all figures but starting with circle.
* The API's code now lives in dir `app` instead of `api` which is picked up
  automatically by FastAPI. This means we can deploy the whole package as-is in
  the Dockerfile and gives consistency between dev, testing and production.

## [0.0.7 - 2022-08-17](https://gitlab.com/thegalagic/figular/-/releases/v0.0.7)

### Added

* Now people can host their own Figular website and API like we do on
  figular.com:
  * New [Hugo Module](https://gohugo.io/hugo-modules/) containing all the web
    layout and JavaScript necessary to host Figures in a Hugo site. Note that we
    depend on the [Wowchemy](https://wowchemy.com/) framework.
  * New Dockerfile for hosting the back end API in a container.
  * Full instructions on how to make it all work:
    [SelfHosting](docs/SelfHosting.md)

### Changed

* The configuration parameter `FIGULAR_API_HOST` in the hugo
  module that tells it where the back end is now includes the protocol as well
  as the domain. This allows people to choose whether to use http or https as
  we did not want to include steps for HTTPS setup in the self-hosting doc. So
  if you had this before in your Hugo `config.yaml`:

```yaml
params:
  figular_api_host: localhost:8081
```

  ...you now need to add the protocol like this:

```yaml
params:
  figular_api_host: http://localhost:8081
```

## [0.0.6 - 2022-08-12](https://gitlab.com/thegalagic/figular/-/releases/v0.0.6)

### Changed

* API: set the timeout on the asy process by environment variable so it can be
  controlled by deployment not code.

## [0.0.5 - 2022-08-11](https://gitlab.com/thegalagic/figular/-/releases/v0.0.5)

### Changed

* Big changes underneath, not yet exposed to end users:
  * Use [asyunit v2](https://gitlab.com/thegalagic/asymptote-glg-contrib/-/releases/v2.0.0)
    for tests which gives better isolation and detects more issues.
  * Evolved our libraries that power the figures. Drawing is expressed in more
    natural language and many more parts are stylable.
  * Use `xelatex` engine instead of `latex` as much better font support.
* All dependencies update to latest

### Removed

* Figure 'board election' has been removed to focus on our core figures. This
  decision was taken to avoid extra work in migrating it to the new changes
  above.

## [0.0.4 - 2022-05-13](https://gitlab.com/thegalagic/figular/-/releases/v0.0.4)

### Added

* New figure 'board election' introduced. See
  [docs](docs/figures/case/boardelection.md) and blog post [A new Figure for the
  OSI Board Election](https://figular.com/post/20220511172059/a-new-figure-for-the-osi-board-election/)
  for more info.
* New form at the cmdline `fig [file]` where you can run any custom Asymptote
  file and easily import our figures, e.g. `import "org/orgchart" as orgchart;`
  This allows anyone to combine existing figures into new pictures.
* Use an explicit 'style reset' in all figures so they all start from the same
  assumptions. This is particularly important now we are combining figures in
  board election.

### Changed

* The cmdline interface has changed so we can accept markdown. Now the first
  argument is either a file or figure and the remaining arguments are fed to the
  figure. You also no longer need to prefix a figure name with a hyphen.
* The input for a Figure is now of type `string[]` instead of `file`.
  Asymptote (I have discovered) will implicitly cast a file to string[] for us.
  This makes life much easier for testing and for reusing existing Figures in
  new pictures as we do not need to create files to pass data around.

### Removed

* We no longer rely on Asymptote's default `stdin` global variable which defines
  `#` as the comment char as we now need to interpret markdown. So comments are
  no longer possible in input (for now).

## [0.0.3 - 2022-02-15](https://gitlab.com/thegalagic/figular/-/releases/v0.0.3)

### Added

* New figure `org/orgchart` for organisational charts. See
  [orgchart](docs/figures/org/orgchart.md) in the docs for details.
* All Figure documentation has been expanded to cover website usage.
* README: direct contributors to our new wiki.

### Fixed

* Figures can accept and cope with all ASCII printable characters as input. We
  apply fuzz testing to this.
* Don't set CORS in the app, better set on network applicances.
* Build: clear out old built packages otherwise twine will try and upload them
  and fail.

### Changed

* Dependencies updated to latest.

## [0.0.2 - 2021-11-10](https://gitlab.com/thegalagic/figular/-/releases/v0.0.2)

### Added

* More detail on the deployment instructions.

### Fixed

* Quick patch to increase asy timeout to 3s which was hitting 1s limit on prod

## [0.0.1 - 2021-11-08](https://gitlab.com/thegalagic/figular/-/releases/v0.0.1)

### Added

* New cmdline flag `--help` to show usage.
* An API using FastAPI so Figular can be hosted and accessible over HTTP.
* GOVERNANCE.md was missing, added benevolent dictator.

### Fixed

* Bugs in figure `concept/circle`:
  * Crash when not given any blobs. Now we will skip drawing.
  * Crash when one blob and middle=true
  * Blobs were drawn on top of each other when only two blobs and middle=true

## [0.0.0 - 2020-04-01](https://gitlab.com/thegalagic/figular/-/releases/v0.0.0)

First version, basic cmdline usage and docs.

### Added

* New figure `concept/circle`, see docs for details.
