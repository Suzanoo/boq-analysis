### **BOQ Analysis used Dash Plotly :**
#### **Setting up:**
- Install [Anaconda](https://docs.anaconda.com/anaconda/install/index.html), [Git](https://github.com/git-guides/install-git) 
- Clone this repository (or directly download)
```
 git clone https://github.com/Suzanoo/boq-analysis.git
```
- Create conda env and activate conda env
```
 conda create --name <ชื่อ env ที่ต้องการ> python=3.10
 conda activate <ชื่อ env ที่ตั้งไว้>
```
- Install packages
```
 pip install -r requirements.txt
```
#### **Run dash board:**
**Note:** .csv and excel file is allow.

Open Terminal(Mac) or Powershell(Windows) or Anaconda prompt.
```
cd <path to the folder boq-analysis>
conda activate <ชื่อ env ที่ตั้งไว้>
python app.py
```