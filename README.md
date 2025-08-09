# New Russian Wine(Новое русское вино)

Site of the craft wine shop "Новое русское вино".

## How to install

Clone repository to your local device. To avoid problems with installing required additinal packages, use a virtual environment, for example:
```bash
python3 -m venv myenv
source myenv/bin/activate
```

Python3.12 should be already installed. Then use pip (or pip3, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

The script uses additinal packages:

_Jinja2==3.1.6_

_pandas==2.3.1_

_dotenv==0.9.9_

After all these manipulations you can run script using something like this:

```bash
python main.py --xlxs_file_name 'your xlsx file name'
```
You will need an xlsx file with content something like this:

|category|wine name|sort|price|picture|action|
|---|---|---|---|---|---|
| white wine | wine name 1 | sort of grape | $1 | 1.jpg | profitable |
| red wine | wine name 2 | sort of grape | $2 | 2.jpg |  |
| drinks | drink name | sort of grape | $5 | 3.jpg |  |
| red wine | wine name 3 | sort of grape | $1 | 4.jpg | profitable |
| drinks | drink name | sort of grape | $4 | 5.jpg |  |
| white wine | wine name 4 | sort of grape | $2 | 6.jpg |  |

Go to the site at [http://127.0.0.1:8000](http://127.0.0.1:8000).

In the settings.py, for safety reasons, environment variables are used to restrict access for credentias, such as: 

* PRODUCT_FILE - name of xlsx file with product contains.

The file with the  contents of these variables isnt included in the repository. To use the script with your credentials, 
you need to create a .env file in the folder with the script, and add into it lines like PRODUCT_FILE=your_file_name.

## Project Goals

The code is written for educational purposes on online-course for web-developers dvmn.org.
