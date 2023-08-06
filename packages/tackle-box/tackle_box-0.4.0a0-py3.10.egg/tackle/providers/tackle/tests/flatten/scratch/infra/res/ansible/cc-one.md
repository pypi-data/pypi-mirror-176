

A couple years ago I started working on a rewrite of cookiecutter, the highest starred code scaffolding tool on GitHub, which after some scope creep and rewrites turned into its own language, albiet domain specific, that I call tackle. What's unique about it is that it is written entirely in json / yaml / toml making it one of a few programmable configuration languages of the likes of jsonnet, dhall, and more recently CUE with the big difference that tackle is serializable, can be easily embedded into existing config files, and doubles as a self documenting declarative CLI, the first that I know of to be created. 

In this article I'd like to introduce the tool, why I made it, and what I see it's future potentially looking like. 

I was first inspired to build tackle rewrite cookiecutter when I was using it and saw that there were over 7 thousand code scaffolding templates on GitHub, each one of them needing to reimplement the same pieces of boilerplate. For instance every repo needs a license which every one of the 7k repos has their own bespoke solution for. So the solution I thought of was to be able to make cookiecutter modular allowing cookiecutter templates to call other cookiecutters that could specialize in things such as creating a template. As a short example of what this would look like, in co


The original purpose of the rewrite was to make a modular code generator as I saw that cookiecutter had over 7 thousand templates, each one of them needing to reimplement the same parts. For instance when generating some project scaffolding, it is normal to prompt the user for what kind of license they want. I thought that a modern code generator should have the ability to call some license generating module and other parts so that the developer can focus on what makes their template unique. So instead of all kinds of logic like you see here in a cookiecutter template, one could now use the tackle-license module with one line of code. 

```yaml
license->: tackle robcxyz/tackle-license --output . 
```

To explain what is going on here, you can 

It took a couple rewrites, but it now finally checks all the boxes I envisioned for the tool and it is finally ready to be released. Its evolution should be a case study in scope creep which I am going to attempt at justifying by the end of the article. Its result is an elegant combination of cookiecutter, jsonnet, and dhall as the first fully serializable programmable configuration language. 

The original purpose of the tool was to make modular code generators but it ended up being far more. Originally, I saw the popularity of cookiecutter templates with over 7 thousand of them existing at the time of writing with each one of them needing things like licenses and other boilerplate that goes into the making of a repo. What I thought of is instead of each template implementing its own license options, you could instead call a license module which would expose a standard set of options. So for instance in cooki

```yaml

```


What I came up with I think is quite elegant in that it has ways of knitting together multiple 



# Rewriting Cookiecutter into a DSL

A couple years ago I was working on a project where I generated code using cookiecutter, the highest starred code scaffolding tool on GitHub, which evolved to the point that I completely rewrote the tool into its own turing complete domain specific language written entirely in json / yaml / toml. It took a couple rewrites, but it now finally checks all the boxes I envisioned for the tool such as being able to build modular code generators and declarative CLIs. 

In this article I will be breifly introducing the tool starting most importantly with why I built it in the first place, then cover a bit of the syntax, and end up with a simple example of how to build a modular code generator. This is the very first article on the tool 

### Project Origin 


- Started working on a customized cookiecutter 
  - Intention was 
    - 
- Code generation is one use case 



Hi, I have been working on a total rewrite of cookiecutter called tackle-box and I'm getting pretty close to releasing it officially. The easiest way to describe it for those that know CC is that instead of custom hooks being in the `hooks/[pre/post]_gen_hook.py`, these hooks are instead called from within the base config file (ie `cookiecutter.json`) to perform all the logic. I have built ~100 of these hooks to do things like prompt a user for inputs, generate code, import / call other tackle providers / hooks, and a whole bunch of other things. Compared to CC, this means that string values are no longer automatically interpreted as prompts and to render code you need to explicitly tell it where the templates / output is. So for instance to create a simple code generator with templates in a `templates` directory, one would do:

```yaml
project_slug->: input 
gen->: generate templates {{project_slug}}
```

This design offers a lot more flexibility as the tool parses arbitrary json / yaml / toml and hooks can be embedded in the document to impose arbitrary logic. Theres a lot more to it and would encourage anyone interested to check it out and give any feedback that you may have. 


---

Hi, I rewrote cookiecutter and thought it was time to comment here. 