#### Core Objective

* Find a project you're interested in
* See if it currently has a code of conduct
* See if it there have been instances of problematic conduct in community
* See if it has underrepresented (women, queer, and trans identifying, people of colour, neurodiverse and disabled folks, etc) contributors or authors
* Submit `Submission`s (see `projects/models.py#Submission`) to projects with a tag such as 'problematic conduct', 'queer contributor', etc
* Highlight projects with diverse communities and a code of conduct
* Vouch for Projects and their Submissions
* Data entry enters a verification queue for moderators to accept before public listing

#### Further Goals

* Optionally public profiles to see Submissions, Projects, and Vouches you've made
    * Identity tags on profiles, attach yourself to a project as a contributor or author, project can be featured as having a maintainer with your identity tags.
      e.g. I identity as queer, I contribute to codeofconductlink, projects/codeofconductlink is shown as having queer contributors.
    * Project icons for PoC, queer, trans contributors, etc (h/t @lynncyrin)
* disqus comments on projects
* GitHub/other badge for project community (“This product has a code of conduct.” etc)
* Project edit history with `django-reversion`


#### Contributing

This project is written with Python 3, Django 1.8.x, and sass.

Assuming you have Python 3 and virtualenvwrapper installed:

```
mkvirtualenv -p $(which python3) codeofconductlink
workon codeofconductlink
git clone $repo
cd codeofconductlink
cp .env.dev.sample .env.dev
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata sample_data.yaml
python manage.py runserver --norecaptcha
```

Sample data gives user/pass combinations of:

* (admin user) `test@admin.com/testing`
* (email verified non-admin user) `test@verified.com/testing`
* (email not verified non-admin user) `test@unverified.com/testing`

You'll need to fill out the `.env.dev` file, grab a reCAPTCHA site and secret key if you want to play with that.

Right now there's no use of an asset pipeline or anything. I just run

`sass --watch static/styles/global.scss:/Users/emily/static/global.css`

(my `.env.dev` contains `STATICFILES_DIR=~/static`)

This obviously needs improvement.

#### Icons

Currently using the [Material Design Icons](http://google.github.io/material-design-icons) from Google with the [Material Design Iconic Font](http://zavoloklom.github.io/material-design-iconic-font/examples.html) project. Not entirely happy with this solution but it's adequate for development right now and the page size is acceptable.

When using icons, please use the `{% icon "zmdi zmdi-label-heart zmd-fw %}` (example) tag so that `aria-hidden` and `role` properties are added.
