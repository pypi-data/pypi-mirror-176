# Jklint

A CLI designed to save time linting Jenkinsfiles by typing a maximum of 2 keywords in the terminal.


## Features ⭐

1.Credentials entered one time only

2.Short commands to type

3.Validate Jenkinsfiles through the official Jenkins API

4.Masked credentials

## Setup 🛠

Jklint can be installed through Pypi or a clone of the repository. 

## From Pypi

The easiest option to setup Jklint is to install the pip package and run it into a virtual environment.

### 1.Create a virtual environment
```
python3 -m venv <virtual-environment-name>
```

### 2.Activate the virtual environment

<table class="docutils align-default">
<colgroup>
<col style="width: 17%">
<col style="width: 16%">
<col style="width: 67%">
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Platform</p></th>
<th class="head"><p>Shell</p></th>
<th class="head"><p>Command to activate virtual environment</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td rowspan="4"><p>POSIX</p></td>
<td><p>bash/zsh</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <span class="pre">source</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/activate</span></code></p></td>
</tr>
<tr class="row-odd"><td><p>fish</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <span class="pre">source</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/activate.fish</span></code></p></td>
</tr>
<tr class="row-even"><td><p>csh/tcsh</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <span class="pre">source</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/activate.csh</span></code></p></td>
</tr>
<tr class="row-odd"><td><p>PowerShell</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/Activate.ps1</span></code></p></td>
</tr>
<tr class="row-even"><td rowspan="2"><p>Windows</p></td>
<td><p>cmd.exe</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">C:\&gt;</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">\Scripts\activate.bat</span></code></p></td>
</tr>
<tr class="row-odd"><td><p>PowerShell</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">PS</span> <span class="pre">C:\&gt;</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">\Scripts\Activate.ps1</span></code></p></td>
</tr>
</tbody>
</table>

### 3.Install the package

```
python3 pip install jklint
```

## Through clone

### 1.Clone the repository
```
git clone https://github.com/aissa-laribi/jklint
```

### 2.Create a virtual environment
```
python3 -m venv <virtual-environment-name>
```
### 3.Activate the virtual environment

<table class="docutils align-default">
<colgroup>
<col style="width: 17%">
<col style="width: 16%">
<col style="width: 67%">
</colgroup>
<thead>
<tr class="row-odd"><th class="head"><p>Platform</p></th>
<th class="head"><p>Shell</p></th>
<th class="head"><p>Command to activate virtual environment</p></th>
</tr>
</thead>
<tbody>
<tr class="row-even"><td rowspan="4"><p>POSIX</p></td>
<td><p>bash/zsh</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <span class="pre">source</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/activate</span></code></p></td>
</tr>
<tr class="row-odd"><td><p>fish</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <span class="pre">source</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/activate.fish</span></code></p></td>
</tr>
<tr class="row-even"><td><p>csh/tcsh</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <span class="pre">source</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/activate.csh</span></code></p></td>
</tr>
<tr class="row-odd"><td><p>PowerShell</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">$</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">/bin/Activate.ps1</span></code></p></td>
</tr>
<tr class="row-even"><td rowspan="2"><p>Windows</p></td>
<td><p>cmd.exe</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">C:\&gt;</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">\Scripts\activate.bat</span></code></p></td>
</tr>
<tr class="row-odd"><td><p>PowerShell</p></td>
<td><p><code class="samp docutils literal notranslate"><span class="pre">PS</span> <span class="pre">C:\&gt;</span> <em><span class="pre">&lt;venv&gt;</span></em><span class="pre">\Scripts\Activate.ps1</span></code></p></td>
</tr>
</tbody>
</table>

### 4.Install dependancies and package locally

```
pip install -e .
```

## Usage

It's recommended to run jklint from a virtual environment, this way the credentials and the Jenkins client will not be found in the repository. Only the Jenkinsfile should be in the repository.

1.Configure jklint

```
jklint config
```

If you work with VS Code and your OS is a POSIX OS, an .env file should open. Otherwise, find the .env file in your current directory(that should your virtual environment directory)

Replace the values with yours and save the file.

2.Validate the file

```
jklint go
```
It will download the Jenkins client from your Jenkins url. Then, it will proceed to the validation of the Jenkinsfile

If the credentials and the syntax of the Jenkinsfile are correct it should return:

```
Jenkins-client found
CompletedProcess(args=['java', '-jar', 'jenkins-cli.jar', '-s', 'jenkins-url', '-webSocket', '-auth', 'user', 'declarative-linter'], returncode=0, stdout='Jenkinsfile successfully validated.\n', stderr='')
```

And your 'user' and 'jenkins-url' details will stay hidden.