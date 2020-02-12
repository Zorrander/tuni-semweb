# Semantics teaching interface

Interface composed of:
* A virtual assembler to teach the semantics of an assembly task.
* A planning scene allowing to visualize a suggested action sequence.
* A chat-like interface to make planning interactive using natural language.


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

The interface is distributed with a Dockerfile.
Follow those [instructions](https://runnable.com/docker/getting-started/) to get docker on your system.

### Installing

Once docker is installed, you are ready to first build your container:

```
docker build -t APP ~/panda_tuni_webapp
```

And you can run it with:

```
docker run --net=host APP
```

You should now be able to [access](127.0.0.1:5000) the interface in your browser.


## Built With

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - The web framework used
* [jena_sempy](https://pypi.org/project/jena-sempy/) - Semantic data management
* [Three.js](https://threejs.org/) - Construct the visual assembler
* [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) - To allow interactions


## Authors

* **Alexandre Angleraud**- [Cognitive Robotics TUNI](https://research.tuni.fi/cogrob/)


## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE.md](LICENSE.md) file for details
