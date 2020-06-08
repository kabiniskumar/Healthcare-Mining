# Data Scraping

We have scraped data from the following health care discussion forums.
1. [WebMd](https://messageboards.webmd.com/)
1. [Patient Info](https://patient.info/forums)
1. [Mayo Clinic](https://connect.mayoclinic.org/groups)



## Follow the below instructions to scrape data from WebMd

### Prerequisites

`pip install scrapy` <br />
`pip install selenium` <br />
`pip install webdriver_manager` <br />
`pip install pickle` <br />
`pip install csv` <br />
`pip install requests` <br />
`pip install bs4` <br />
`pip install csv` <br />

### Run the command below to scrape data from WebMd

`scrapy runspider webmd_scraper.py -o <output_file_name> `

### Run the command below to scrape data from PatientsInfo

`scrapy runspider patients_info_scraper.py -o <output_file_name>`

### Run the commands below to scrape data from Mayo Clinic

`py mayo_clinic_get_links.py` <br />
`py mayo_clinic_scraper.py`

Scraped data will be generated in the following format

**<condition,postLink,postHeading,postContent>**

The output files generated can be passed on to the MetaMap module to identify diseases and symptoms