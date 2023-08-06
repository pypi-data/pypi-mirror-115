# nore -- Completely Unnecessary .gitignore Management

## Features

* Supports 128 environments and growing
* Optionally specify a location for the .gitignore file

## Planned Features

* Add support for github/gitignore/Global .gitignore templates
* Add support for github/gitignore/community .gitignore templates
* Option to merge .gitignore files together rather than overwrite
* Detect and merge into a user's global .gitignore
* Add completions

## Installation

Install nore by running:

```shell
pip install nore
```
or better yet

```shell
pipx install nore
```

## Usage

```
Usage: nore [OPTIONS] [LANGUAGE]

Arguments:
  [LANGUAGE]  Language for created .gitignore file.

Options:
  -l, --list               List available .gitignore language.
  --output-path DIRECTORY  Where to create the .gitignore file.

  --install-completion     Install completion for the current shell.
  --show-completion        Show completion for the current shell, to copy it
                           or customize the installation.

  --help                   Show this message and exit.
```

Create a python .gitignore file in the current directory by running
```shell
>> nore new python
Created .gitignore at .
```

List all available .gitignore types by running
```shell
>> nore list
actionscript              godot                     python               
ada                       gradle                    qooxdoo              
agda                      grails                    qt                   
android                   gwt                       r                    
appceleratortitanium      haskell                   rails                
appengine                 idris                     raku                 
archlinuxpackages         igorpro                   rhodesrhomobile      
autotools                 java                      ros                  
c                         jboss                     ruby                 
c++                       jekyll                    rust                 
cakephp                   jenkins_home              sass                 
cfwheels                  joomla                    scala                
chefcookbook              julia                     scheme               
clojure                   kicad                     scons                
cmake                     kohana                    scrivener            
codeigniter               kotlin                    sdcc                 
commonlisp                labview                   seamgen              
composer                  laravel                   sketchup             
concrete5                 leiningen                 smalltalk            
coq                       lemonstand                stella               
craftcms                  lilypond                  sugarcrm             
cuda                      lithium                   swift                
d                         lua                       symfony              
dart                      magento                   symphonycms          
delphi                    maven                     terraform            
dm                        mercury                   tex                  
drupal                    metaprogrammingsystem     textpattern          
eagle                     nanoc                     turbogears2          
elisp                     nim                       twincat3             
elixir                    node                      typo3                
elm                       objective-c               umbraco              
episerver                 ocaml                     unity                
erlang                    opa                       unrealengine         
expressionengine          opencart                  visualstudio         
extjs                     oracleforms               vvvv                 
fancy                     packer                    waf                  
finale                    perl                      wordpress            
forcedotcom               phalcon                   xojo                 
fortran                   playframework             yeoman               
fuelphp                   plone                     yii                  
gcov                      prestashop                zendframework        
gitbook                   processing                zephir               
go                        purescript                                     
```

