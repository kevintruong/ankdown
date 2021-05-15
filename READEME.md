# README

Convert anki apkg file to markdown repository. The anki apik using zip and sqlite to compact the cards deck. APKG file
can content multiple decks file. Each deck file content multiple cards. Each card can have different model defile by
model field.

The anki converter support to analyze the anki apkg format and support user can define template to export an anki apkg
to markdown

## Command

### Generate deck template format file

```shell
anki_converter gen_template --apkg_file <anki apkg file> --output <output dir> 
```

* `gen_template` command to generate template decks markdown file format
* `--input` input apkg file
* `--output` output directory

#### card model schema file

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

### Export markdown deck

```shell
anki_converter export --apkg_file <working dir> 
```

Create new folder content the decks and its sub decks (if exists). the command will input template file and generate
deck file (markdown) follow the defined template. 






