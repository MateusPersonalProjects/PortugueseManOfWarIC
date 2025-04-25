# PortugueseManOfWarIC

![Linux](https://img.shields.io/badge/Linux-E34F26?style=for-the-badge&logo=linux&logoColor=black)
![Python programming language](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

<div align="center">
<img src="repoImage.png" alt="PortugueseManOfWarIC Project image">
</div>

>The repository `PortugueseManOfWarIC` contains data cleaning scripts focused on date and location fields.  
These scripts were developed to support a case study on sightings of Portuguese man o' war (Physalia physalis) along the Brazilian coastline.

## Requirements

Before you start,  make sure you have all the requirements:

- The latest version of `Python3`
- A computer running `Linux`.

## Installing <PortugueseManOfWarIC>

To install <PortugueseManOfWarIC>, follow these steps:

Linux:

First, clone the repository:

```
git clone https://github.com/MateusPersonalProjects/PortugueseManOfWarIC.git
```

Navigate to the project directory:
```
cd PortugueseManOfWarIC
```

Create a virtual environment:
```
pip -m venv myenv
```

Activate the virtual environment:
``` 
source myenv/bin/activate
```

Install all requirements:
```
pip install -r requirements.txt
```

## ⚠️ Important

The googleScript.py script assumes your dataset contains the following column names:

- `Geolocation`
- `Location`
- `State`

If your dataset uses different column names, you **must modify the function** `searchStringBuilder()` directly in the code to match the names used in your database.


## Contributing to PortugueseManOfWarIC

To contribute to PortugueseManOfWarIC, follow these steps:

1. Fork this repository.
2. Create a branch: `git checkout -b <branch_name>`.
3. Make your changes and commit them: `git commit -m '<commit_message>'`
4. Push to the original branch: `git push origin <project_name>/<location>`
5. Create the pull request.

Alternatively, see the GitHub documentation on [how to create a pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

## License

This project is licensed under the [MIT License](LICENSE).  
You are free to use, modify, and distribute this code with proper attribution.
