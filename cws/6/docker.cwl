#!/usr/bin/env cwl-runner

cwlVersion: v1.0
class: CommandLineTool
baseCommand: python
hints:
  DockerRequirement:
    dockerPull: python:3
inputs:
  src:
    type: File
    inputBinding:
      position: 1
outputs:
  example_out:
    type: stdout
stdout: output.txt