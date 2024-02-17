# writing blog on deploying the web app on AWS
***Brief overview of the blog’s purpose: deploying a Django project on AWS EC2.***
 ***Importance of deploying Django projects on scalable and reliable platforms like AW***S.
So today we are going to deploy an existing project made in python on AWS server. So the project I am going to deploy is a simple Django project I previously created for a user management tutorial here on medium itself. Here's the link to that article if you are interested: []
## Prerequistes:
So this tutorial assumes that you atleast have a working knowledge of how websites work(backend, frontend and database). Next you should have a simple project created that you want to be able to deploy on AWS(prefferably Django). Some knowledge of what AWS is and What is ec2 instance on AWS would be great but otherwise we will briefly discuss about that in just a minute. 

## jargons
Let's first get a few jargons out of the way so it become easier for you to navigate through this tutorial:
-- choose few jargons out of these:
1. **Web Server Gateway Interface (WSGI)**: WSGI is a specification that describes how a web server communicates with web applications, such as Django. It defines a standard interface for handling web requests.
    
2. **Gunicorn**: Gunicorn is a WSGI server that is commonly used to serve Django applications in production. It can handle multiple concurrent requests efficiently.
    
3. **Virtual Environment (virtualenv)**: A virtual environment is a self-contained directory that contains a Python installation and any necessary libraries for a specific project. It helps isolate project dependencies from other Python projects.
    
4. **Static files**: Static files are files such as CSS, JavaScript, and images that are served directly to the client without being processed by the Django application. These files are typically stored in a directory specified in the `STATICFILES_DIRS` setting and served using a web server like Nginx or AWS S3.
    
5. **Database Migration**: Database migration is the process of applying changes to the database schema as defined in Django models. Django provides a built-in migration system that allows you to create, apply, and revert migrations.
    
6. **Amazon S3**: Amazon Simple Storage Service (S3) is a scalable storage service provided by AWS. It is commonly used to store static files for web applications due to its durability and scalability.
    
7. **Amazon RDS**: Amazon Relational Database Service (RDS) is a managed database service provided by AWS. It supports multiple database engines and is commonly used to host the database for Django applications.
    
8. **Amazon EC2**: Amazon Elastic Compute Cloud (EC2) is a web service that provides resizable compute capacity in the cloud. It is commonly used to host web applications, including Django applications.
    
9. **Elastic IP**: An Elastic IP address is a static IPv4 address designed for dynamic cloud computing. It allows you to mask the failure of an instance or software by rapidly remapping the address to another instance in your account.
    
10. **Load Balancer**: A load balancer is a device or service that distributes incoming traffic across multiple servers to ensure that no single server is overwhelmed. AWS provides Elastic Load Balancing (ELB) service for this purpose.
    
11. **Auto Scaling**: Auto Scaling helps you maintain application availability and allows you to automatically add or remove EC2 instances based on conditions you define. It helps ensure that your application can handle varying levels of traffic.
12. **AWS EC2**: Amazon Elastic Compute Cloud (EC2) is a web service that provides resizable compute capacity in the cloud. It is designed to make web-scale cloud computing easier for developers.
    
2. **Instance**: An EC2 instance is a virtual server in the AWS cloud. It can be configured with various CPU, memory, storage, and networking capacities to meet the requirements of your application.
    
3. **AMI**: An Amazon Machine Image (AMI) is a template that contains the software configuration (operating system, application server, and applications) required to launch an EC2 instance.
    
4. **Security Group**: A security group acts as a virtual firewall for your EC2 instances to control inbound and outbound traffic. You can specify which traffic is allowed to reach your instances.
    
5. **Key Pair**: A key pair consists of a public key and a private key. You use the private key to access your EC2 instances securely using SSH (Secure Shell).
    
6. **Elastic IP**: An Elastic IP address is a static IPv4 address designed for dynamic cloud computing. It allows you to mask the failure of an instance or software by rapidly remapping the address to another instance in your account.
    
7. **Elastic Load Balancer (ELB)**: ELB automatically distributes incoming application traffic across multiple EC2 instances to improve fault tolerance and scalability of your application.
    
8. **Auto Scaling**: Auto Scaling helps you maintain application availability and allows you to automatically add or remove EC2 instances based on conditions you define.
    
9. **Route 53**: Route 53 is a scalable domain name system (DNS) web service designed to route end users to Internet applications by translating domain names into IP addresses.
    
10. **RDS**: Amazon Relational Database Service (RDS) is a web service that makes it easier to set up, operate, and scale a relational database in the cloud. It supports multiple database engines like MySQL, PostgreSQL, etc.

Let's jump right into it and learn along the way:
## Login to AWS and create EC2 instance
Create a AWS account if you already do not have one.
Login into your account and go to services section and from there select EC2.
![](Pasted%20image%2020240216131335.png)
click on launch instance.
Now you can name your instance anything you want e.g. I have named it `Django_Deployment` as seen in here below. Then continue choosing your AMI(Amazon Machine Image), I prefer Ubuntu but you can go ahead and choose any(But be careful, not all AMIs are eligible for free tier. But Ubuntu is so it wont be a problem for us). Then we choose instance type, which you can choose based on your current requirement but I will go ahead and choose `t2.micro` which again is eligble for free tier.
Now we need to generate a key pair for our instance which will help us connect with our instance remotely(Be careful where you place this key pair, you will get this only once, if you lose it you will have to generate it again). But AWS also provides us a way to interact with our instance right through the browser, for which we do not require key pair, although its not recommended but later in the tutorial I will show you how to just do that.
![](Pasted%20image%2020240216132247.png)
Now select create security group option and create these two security groups:
![](Pasted%20image%2020240216133228.png)
the first will allow you to connect to your instance remotely and the second is for anyone on the internet to access your website(You can remove HTTP security rule for now if you want, you can always add that later)
Let's leave all other details to default for now.
Click launch instance and Voila![party emoji] your first EC2 instance is created. Now go back to your instances dashboar and you should see the instance there, dont worry it will take a few minutes to launch and when it does you will see something like this:
![](Pasted%20image%2020240216133614.png)

## connect to instance using ssh
Select the instance and click on connect in top-center. You will be redirected to ssh connection page, here you either can connect directly through your browser window or you can connect using your Operating system's terminal using the key pair file like below:
![](Pasted%20image%2020240216233520.png)
Go to the directory where your `.pem` file is located and run the commands shown above. And you should be connected to your instance by now.(Note: the chmod command will work only on linux distros So you can use git bash to run windows)

## preparing the project  for deployment

Before deploying your Django project to AWS EC2, you need to prepare it for deployment. This involves collecting static files and ensuring that your project is configured correctly for the production environment.

1. Add `STATIC_ROOT` variable to `settings.py` and set it to the directory where you want to store static files. For example:
   ```python
   STATIC_ROOT = os.path.join(BASE_DIR, 'static')
   ```
   This tells Django to collect static files into the `static` directory within your project's base directory.
2. **Collect Static and Media Files:**
   - In your local Django project directory, run the following command to collect static files into the `STATIC_ROOT` directory (defined in your settings):
     ```
     python manage.py collectstatic
     ```
   - This command gathers all static files from your project's apps and third-party packages into a single directory for serving by the web server.
   - additionally, add the following code to your `settings.py` file to configure media files(user uploaded files):
     ```python
     MEDIA_URL = '/media/'
     MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
     ```

2. **Configure Settings for Production:**
   - Update the `ALLOWED_HOSTS` setting in your Django settings file (`settings.py`) to include the domain or IP address of your AWS EC2 instance. For example:
     ```python
     ALLOWED_HOSTS = ['your-instance-public-dns', 'your-domain.com']
     ```
   - Ensure that your `DEBUG` setting is set to `False` for production:
     ```python
     DEBUG = False
     ```

3. 

## installing required dependencies on EC2 instance
Connect to your EC2 instance using the following:
```bash
ssh -i /path/to/your-key.pem ec2-user@your-instance-public-dns
```

