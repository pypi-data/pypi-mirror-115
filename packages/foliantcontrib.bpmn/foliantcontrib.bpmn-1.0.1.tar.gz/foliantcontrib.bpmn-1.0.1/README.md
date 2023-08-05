[![](https://img.shields.io/pypi/v/foliantcontrib.bpmn.svg)](https://pypi.org/project/foliantcontrib.bpmn/) [![](https://img.shields.io/github/v/tag/foliant-docs/foliantcontrib.bpmn.svg?label=github)](https://github.com/foliant-docs/foliantcontrib.bpmn)

# BPMN Diagrams Preprocessor for Foliant

[BPMN (Business Process Modeling Notation)](https://www.bpmn.org/) is visual modeling language for documenting business workflows. This preprocessor converts BPMN diagram definitions in source markdown files and converts them into images on the fly during project build.

This preprocessor uses [bpmn-to-image](https://github.com/bpmn-io/bpmn-to-image) tool by [bpmn.io](https://bpmn.io/) to convert diagrams into images.

## Installation

```bash
$ pip install foliantcontrib.bpmn
```

You will also need to install bpmn-to-image:

```bash
$ npm install -g bpmn-to-image
```

## Config

To enable the preprocessor, add `bpmn` to `preprocessors` section in the project config:

```yaml
preprocessors:
    - bpmn
```

The preprocessor has a number of options:

```yaml
preprocessors:
    - bpmn:
        cache_dir: !path .diagramscache/bpmn
        converter_path: bpmn-to-image
        format: png
        as_image: true
        params:
            no-title: true
        `fix_svg_size`: false
```

`cache_dir`
:   Path to the cache directory for the generated diagrams. It can be a path relative to the project root or a global one.

>   To save time during build, only new and modified diagrams are rendered. The generated images are cached and reused in future builds.

`converter_path`
:   Path to bpmn-to-image binary. By default, it is assumed that you have the `bpmn-to-image` command in your `PATH`, but if it is not the case you can define it here. Default: `bpmn-to-image`

`format`
:   Output format of the diagram image. [Available formats](https://github.com/bpmn-io/bpmn-to-image) at the time of writing: `pdf`, `png`, `svg` (note that most backends won't render `pdf` as image). Default: `png`

`as_image`
:   If `true` — inserts the diagram into the document as Markdown-image. If `false` — inserts the svg code of the diagram directly into the document (works only for `svg` format). Default: `true`

`params`
:   Params passed to the bpmn-to-image tool. Value of this option must be a YAML-mapping. Params which require values should be specified as `param: value`; params which don't require values should be specified as `param: true`:

        preprocessors:
            - bpmn:
                params:
                    no-footer: true
                    min-dimensions: '500x300'

> To see the full list of available params, run the `bpmn-to-image` command without parameters.

`fix_svg_size`
:   Works only with `svg` format and `as_image: false`. By default svg is embedded with hardcoded width and height so they may exceed the boundaries of your HTML page. If this option is set to `true` the svg width and height will be set to `100%` which will make it fit inside your content container. Default: `false`.


## Usage

To insert a diagram definition in your Markdown source, enclose it between `<bpmn>...</bpmn>` tags:

```html
Here’s the diagram:

<bpmn>
    <?xml version="1.0" encoding="UTF-8"?>
    <definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:omgdc="http://www.omg.org/spec/DD/20100524/DC" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="sid-38422fae-e03e-43a3-bef4-bd33b32041b2" targetNamespace="http://bpmn.io/bpmn" exporter="http://bpmn.io" exporterVersion="0.10.1">
      <process id="Process_1" isExecutable="false">
        <task id="Task_0l0q2kz" name="Single Task" />
      </process>
      <bpmndi:BPMNDiagram id="BpmnDiagram_1">
        <bpmndi:BPMNPlane id="BpmnPlane_1" bpmnElement="Process_1">
          <bpmndi:BPMNShape id="Task_0l0q2kz_di" bpmnElement="Task_0l0q2kz">
            <omgdc:Bounds x="206" y="108" width="100" height="80" />
          </bpmndi:BPMNShape>
        </bpmndi:BPMNPlane>
      </bpmndi:BPMNDiagram>
    </definitions>
</bpmn>
```

You can override preprocessor parameters in the tag options. For example if the format for diagrams is set to `png` in foliant.yml and you need one of your diagrams to render in svg, override the `format` option in the tag:

```html
SVG diagram:

<bpmn format="svg">
...
</bpmn>
```

Tags also have an exclusive option `caption` — the markdown caption of the diagram image.

```html
Diagram with a caption:

<bpmn caption="Diagram of the supply process">
...
</bpmn>
```
