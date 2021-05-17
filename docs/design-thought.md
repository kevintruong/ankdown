# Design thought

The tool will help on export anki apkg file to markdown repository. there have two thing need to clarify. The model of
cards in anki apkg and how the user want the model render to.

To help user can export the apkg to markdown as they expected. User need to declare a template file which allows the
tool can render correct markdown based on template file

the template file will use [jinja2](https://jinja.palletsprojects.com/en/3.0.x/templates/)

```jinja2
{# comment #} 

{# model fields #} 
{# cardname, image , audio , define, question, options  ... } 

## {{ cardname }} 

{{ image }}

---- {# card split #}

{{ audio }} 

---- 

{{ define }} 

----

{{ question }} 

{# we can define macro here to process options values 
{{ options }} 


```

The process including 3 steps:

* Generate model jinja2 template file from models in anki apkg
* User custommizes the jinja2 template file.
* Generate markdown decks based on customized template file


