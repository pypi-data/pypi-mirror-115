# Framework detector

Detects which framework is in use for a project and suggests a dockerfile.

Strongly influenced by https://github.com/netlify/framework-info

## Installation

```sh
pip install framework-detector
```

## Usage

```python
from framework_detector import detector, get_dockerfile
from pathlib import Path

framework = detector.detect(Path.cwd())

dockerfile = get_dockerfile(framework["dockerfile"])
```