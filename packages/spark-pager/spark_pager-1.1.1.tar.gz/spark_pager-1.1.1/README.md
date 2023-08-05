
# spark-pager

265, ```You got Mail```

A 'tongue-in-cheek' pager of some sorts that notifies users via email alerts on the status of Spark Jobs during/after execution 


## Prerequisites
* An E-mail Address and Password
## Installation

Install spark-pager with pip

```bash
  pip install spark-pager
```
    
## Usage

* Import and instantiate package with e-mail credentials and spark context
```python
from spark_pager import Pager
from pyspark import SparkContext

sc = SparkContext()

pager = Pager(spark_context=sc, 
              username = <username>, 
              password = <password>,
              host = <host>,
              port = <port>)

## monitor the spark-context when spark-jobs are initiated 
## and notify users on its status.

pager.listener()

```

💥 Note: the default host is ```smtp.gmail.com```
          and the default port is ```587```; feel free to revert to the host and port of your choosing


* To Stop the pager; run this .::

```python
# To stop the pager
pager.stop()

# To stop the spark-context
sc.stop()
```

### Example-Code
```python
## Import Packages
from spark_pager import Pager
from pyspark import SparkContext
from pyspark.sql import SparkSession

## Set Spark Configuration
sc = SparkContext()
spark = SparkSession.builder \
                    .enableHiveSupport() \
                    .getOrCreate() 

spark.sparkContext.setLogLevel("ERROR")
spark.conf.set("spark.sql.repl.eagerEval.enabled", True)

## Intialize Pager 
pager = Pager(spark_context=sc, 
              username = user@gmail.com, 
              password = password)

## Set Listener
pager.listener()

df = spark.createDataFrame([("john-doe", 34), 
                            ("jane-doe", 22)], 
                            ["name", "age"])

# Stop Pager
pager.stop()

# Stop Spark-Context
sc.stop()          
```

💥 Note: Job Status could either be ```Running```, ```Failed``` or ```Succeeded```

Now if everything goes well; you should receive a mail notification that looks kind-of like this .::

![alt text](https://github.com/BrightEmah123/spark-pager/blob/main/test/spark-pager.jpg?raw=true)


## Appendix

This project is open to contributions and additions from the community


## Authors

- [@bright_emah](https://www.github.com/BrightEmah123)

  