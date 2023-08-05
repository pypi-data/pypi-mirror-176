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

# Self Hosting

These instructions will walk you through creating and hosting your own Figular
website similar to that at [Figular](https://figular.com/). We'll also spin up a
back end Figular API that the website will use to render figures - all hosted on
infrastructure you control.

If you just want to use Figular at the cmdline then it's much easier to
install it locally with pip. The cmdline version is completely self-contained
and does not require any network traffic (aside from the install process). See
the project's [README](https://gitlab.com/thegalagic/figular) for how to do that.

Let's get started. These steps are longer and more complex then I'd like but
we've got to start somewhere. There are two parts we need to get running:

* Back End API
* Front End Website

Prerequisites:

* [Podman](https://podman.io/) or [Docker](https://www.docker.com/get-started/)
  to build the back end container. We'll also use this to run it in this doc but
  you can of course use any container platform.
* [Hugo](https://gohugo.io/) to build and (initially) host the website, though
  you can host it however you like once the site is built.
  See [Install Hugo](https://gohugo.io/getting-started/installing). Version
  0.95+ is recommended.

## Back End API

We are going to build and deploy the figular container with podman (or docker).
The [figular](https://gitlab.com/thegalagic/figular) repo contains a
[Dockerfile](https://gitlab.com/thegalagic/figular/-/blob/main/Dockerfile) you
can use. Check out the repo and cd into it. Then run:

```bash
podman build -t figular .
podman run -d -p 8080:8080 localhost/figular:latest
```

You can swap podman for docker above if using it instead.

Check it's up by hitting the status end point:
[http://localhost:8080/status](http://localhost:8080/status) which should give
a 'null' JSON result if it's responding.

## Front End Website

Next we'll create a Hugo website:

```bash
hugo new site DESTDIR
cd DESTDIR
```

Figular is available as a Hugo [Module](https://gohugo.io/hugo-modules/). To add
it to our new site we must first initialise our site as a module itself:

```bash
hugo mod init [YOUR MODULE NAME e.g. gitlab.com/me/myfigularsite]
```

Your module name does not really matter at this stage and you can change it
later.

Now to add Figular and it's dependency on the Wowchemy Hugo Theme put the
following to the end of your `config.toml`:

```toml
[module]
[[module.imports]]
path = 'gitlab.com/thegalagic/figular/hugo'
[[module.imports]]
path = 'github.com/wowchemy/wowchemy-hugo-themes/modules/wowchemy/v5'
```

Now let's check Hugo can fetch those modules ok:

```bash
hugo mod get
```

That should complete ok, any problems please let me know.

Due to [Breaking changes in Hugo 0.91.0](https://github.com/wowchemy/wowchemy-hugo-themes/discussions/2559)
please also add the following to the end of `config.toml`:

```toml
[security.funcs]
  getenv = ["^HUGO_", "^WC_"]
```

Now we can make a first post on the website and populate it with a Figular
circle figure as an example:

```bash
mkdir -p content/posts/my-first-post
cat > content/posts/my-first-post/index.md << EOF
---
title: "Circle"
summary: ""  # Add a page description.
type: "widget_page"
---
EOF
cat > content/posts/my-first-post/circle.md << EOF
---
widget: "figular"
headless: true
active: true
weight: 10
title: Circle
help: Enter concepts below to illustrate in a circle.
help_link: https://gitlab.com/thegalagic/figular/-/blob/main/docs/figures/concept/circle.md
data_area_id: concepts
data_area_label: Concepts
figure_url: concept/circle
example_content: |-
  Democracy
  Freedom
  Inclusiveness
  Membership
  Consent
  Voting
  Right to life
design:
  columns: '1'
---
EOF
```

Above in `circle.md` you can customise all fields except for `widget`.
`figure_url` needs to correspond to a final URL fragment that identifies one of
our figures e.g. `concept/circle` or `orgchart/org`. For all the choices see
[Figures](https://gitlab.com/thegalagic/figular/-/blob/main/docs/Figular.md#figures).
You can also add an initial example image to show the user before the first
figure is generated:

```toml
example_media: 'media/example.png'
```

To build and host our new site, run hugo server:

```bash
> hugo server
...
Web Server is available at URL
```

It'll let you know the URL where your content is served so open a browser and
navigate to our new post. The URL will be something like:
[http://localhost:1313/posts/my-first-post/](http://localhost:1313/posts/my-first-post/)

You should see something now, but it will complain that the back end is down. So
the last thing to do is point the website at the back end.

Back in `config.toml` add the following to point the website at our back end we
setup earlier:

```toml
[params]
  figular_api_host = 'http://localhost:8080'
```

Hugo should reload automatically and back in the browser the post should refresh
and no longer show any problems. You can now interact with the figure and it'll
return results from the back end.

There is another optional configuration setting `figular_figure_timeout_ms`.
This sets the time we wait for results from the backend before showing an error:

```toml
[params]
  figular_api_host = 'http://localhost:8080'
  figular_figure_timeout_ms: 10000
```

It's in milliseconds and defaults to 10,000ms (10 seconds).

From this point on you it's up to you how you customise your new site. See the
[Hugo Documentation for Wowchemy](https://wowchemy.com/docs/) for how work with
the Wowchemy framework or get in touch with us if you have questions.
