

### 1. Requirements
- python 3
- python3-venv


Debian/Ubuntu
```sh
apt-get install python3-venv python3-pip
```

MacOs
```sh
brew install python3 python3-venv python3-pip
```



### 2. Setup environment
```sh
$: mkdir project && cd project
$: python3 -m venv venv
$: source venv/bin/activate
$: pip install -r requirements.txt
```

### 3. Launch the script
```sh
(venv) $: ./script.py -f <input_file> -o <results_file>
```


# Additional info
Use `test.txt` file to quickly check the execution results on simple data