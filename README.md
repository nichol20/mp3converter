## Requirements

You must have [kind](https://kind.sigs.k8s.io/) and [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) installed

## How to run

first create a cluster with kind

```bash
kind create cluster --config=cluster-config.yaml
```

permission for the bash script that applies the nginx ingress

```bash
chmod +x ./apply-ingress-controller.sh 
```

run it and wait for it to be ready

```bash
./apply-ingress-controller.sh 
```

apply the manifests for each service with the kubectl and wait until they are ready
```bash
find . -type d -name manifests -exec kubectl apply -f {} \;
```

**you may want to inspect them with the [k9s](https://k9scli.io/) tool**

## How to test

**Before continuing, if you want to receive the IP address of the file to download by email, you will need to configure a few things.**

1 - You need to have an email address and a password to serve as the sender for the notification service.
- One way is through the Google account application password manager: [apppassword](https://myaccount.google.com/u/1/apppasswords)

2 - configure the secret.yaml file in the notification service by replacing the `GMAIL_ADDRESS` and `GMAIL_PASSWORD` variables with your email and the password you created in Google's apppassword respectively.

3 - make sure that the user you are creating in the application has the same email that you want to receive the notification (it can be the same email where you set the application password)

-----
</br>

Before testing you need to map the application url to localhost in hosts. Adding this line:

```
127.0.0.1       mp3converter.com
```

the path in linux is `/etc/hosts` and in windows is `C:\Windows\System32\drivers\etc\hosts`</br>
**If you are using wsl to run a linux system, you can choose which one you want to change.**

</br>

now create the user with curl command

```bash
curl -X POST "http://mp3converter.com/user" -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "MySecurePass"}'
```

login and copy the access token

```bash
curl -X POST "http://mp3converter.com/login" -u user@example.com:MySecurePass
```

send the .mp4 file

```bash
curl -X POST -F 'file=@./example.mp4' -H 'Authorization: Bearer <token>' http://mp3converter.com/upload
```

#### Option 1: If You Have Configured Email and `secret.yaml`
1. Copy the file ID you received via email.
2. Download the file using the following command:

    ```bash
    curl --output example.mp3 -X GET -H 'Authorization: Bearer <token>' "http://mp3converter.com/download?fid=<file_id>"
    ```
3. Play the downloaded MP3 file to ensure it works.

#### Option 2: If You Have Not Configured Email
1. Access the MongoDB container:

    ```bash
    kubectl exec -it mongodb-0 -- bash
    ```

2. Run the following commands to retrieve the file ID:

    - Open MongoDB shell:
        ```
        mongosh
        ```
    - Switch to the mp3s database:
        ```
        use mp3s
        ```
    - List the files to find the file ID:
        ```
        db.fs.files.find()
        ```
    - Copy the file ID from the output, then exit MongoDB shell:
        ```
        exit
        ```

3. Download the file directly from MongoDB using the file ID:

    ```bash
    mongofiles --db=mp3s get_id --local=test.mp3 '{"$oid": "file_id"}'
    ```

4. Exit the container:
    ```
    exit
    ```

5. Copy the file from the MongoDB container to your current directory:
    ```bash
    kubectl cp mongodb-0:/test.mp3 ./test.mp3 
    ```

6. Play the downloaded MP3 file to ensure it works.

## Other tests


- If you want to test the MySQL database, enter the container using this command and type `mysql` when asked for the password

    ```bash
    kubectl exec -it mysql-0 -- mysql -u root -p
    ```

    - the database used is `auth`, so run this command to use it
        ```sql
        USE auth;
        ```
    - and run commands like:
        ```sql
        SELECT * FROM user;
        ```

- If you want to access the rabbitmq management interface, you will have to add this line to your hosts file
    ```
    127.0.0.1       rabbitmq-manager.com
    ```

    - then go to https://rabbitmq-manager.com/ (will appear as not secure, so you will need to click continue to access the site)