### **BOQ Analysis used Dash Plotly :**
#### **Setting up:**
- Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html), [Git](https://github.com/git-guides/install-git) 
- Clone this repository (or directly download)
```
 git clone https://github.com/Suzanoo/boq-analysis.git
```
- Create conda env and activate conda env (You can use pipenv or virtualenv instead)
```
 conda create --name <your env name> python=3.10
 conda activate <your env name>
```
- Install dependencies
```
 pip install -r requirements.txt

 or you can use setup tools instead by run code below
 python setup.py install
```
#### **Run dash board:**
**Note:** .csv and excel file is allow.

Open Terminal(Mac) or Powershell(Windows) or Anaconda prompt.
```
cd <path to the folder boq-analysis>
conda activate <your env name>
python app.py
```
See Heroku App [https://boq-demo.herokuapp.com/](https://boq-demo.herokuapp.com/)