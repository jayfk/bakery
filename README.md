# bakery

Bakery is a cookiecutter render server. It takes JSON and returns rendered cookiecutter templates as zipfiles.

## Usage

Clone the project:
 
    git clone https://github.com/jayfk/bakery.git
    
Add the cookiecutter templates you want to use to `cookiecutters.txt`:

```
https://github.com/pydanny/cookiecutter-django.git
https://github.com/audreyr/cookiecutter-pypackage.git
```

Start the server in development mode:

    docker-compose -f dev.yml up
    
Open your browser and go to [localhost:5000](http://localhost:5000) to see the list of your installed cookiecutters:

```
{
  "cookiecutters": {
    "cookiecutter-pypackage": {
      "cookiecutter.json": {
        "command_line_interface": [
          "Click", 
          "No command-line interface"
        ], 
        "create_author_file": "y", 
        "email": "aroy@alum.mit.edu", 
        "full_name": "Audrey Roy Greenfeld", 
        "github_username": "audreyr", 
        "open_source_license": [
          "MIT license", 
          "BSD license", 
          "ISC license", 
          "Apache Software License 2.0", 
          "GNU General Public License v3", 
          "Not open source"
        ], 
        "project_name": "Python Boilerplate", 
        "project_short_description": "Python Boilerplate contains all the boilerplate you need to create a Python package.", 
        "project_slug": "{{ cookiecutter.project_name.lower().replace(' ', '_') }}", 
        "pypi_username": "{{ cookiecutter.github_username }}", 
        "use_pypi_deployment_with_travis": "y", 
        "use_pytest": "n", 
        "version": "0.1.0"
      }, 
      "path": "/cookiecutters/cookiecutter-pypackage"
    }
  }
}
```

To render a template, send a `POST` request to the server. The request needs to contain

 - 1. the cookiecutter template you want to use 
 - 2. the `cookiecutter.json` values you want to change
 
as JSON parameters.

For example, to render a **cookiecutter-django** template with a **project_name** of **foo**:

    http POST http://localhost:5000/ cookiecutter=cookiecutter-django project_name=foo > project.zip

## State of the project

This is a proof of concept at this point. It's insecure, don't run this in anywhere near production. 