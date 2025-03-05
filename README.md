# EnergyPlus-API

This repository contains code and resources for working with EnergyPlus and running simulations through an API using Colab and Python.

## Overview

[EnergyPlus](https://energyplus.net/) is a building energy simulation program for modeling building heating, cooling, lighting, ventilating, water use, and other energy flows. This repository provides tools and examples for interacting with the EnergyPlus API.

## Get Started Locally

To get started, clone the repository and install the required dependencies:

```bash
git clone https://github.com/MohamedAbdelfattah022/EnergyPlus-API.git
cd EnergyPlus-API
pip install -r requirements.txt
```
Ensure you have EnergyPlus software installed.

## Using Colab
Feel free to use the provided [Colab notebook](EnergyPlus_API%20Colab.ipynb).

Make sure to add the Ngrok Authentication Token to Colab secrets with the name `NGROK_AUTH_TOKEN`.

## Usage

### Running the API Server

To run the API server, execute the following command:

```bash
python EnergyPlus_API.py
```

The server will be accessible at `http://127.0.0.1:8080`.

### API Endpoints

#### 1. Run Simulation

**Endpoint:** `/api/run-simulation`  
**Method:** `POST`  
**Description:** Runs an EnergyPlus simulation with the provided IDF and EPW files.

**Request:**
- `idf_file`: The IDF file (Input Data File) for the simulation.
- `epw_file`: The EPW file (Weather Data File) for the simulation.

**Response:**
- On success, returns the `eplustbl.htm` file, which contains the simulation results.
- On error, returns an error message with the status code.

**Example:**

```bash
curl -X POST -F 'idf_file=@path/to/file.idf' -F 'epw_file=@path/to/file.epw' http://127.0.0.1:8080/api/run-simulation
```

## Docker Deployment

### Dockerfile Details
This project includes a `Dockerfile` to containerize the API.

#### Build the Docker Image
Run the following command to build the Docker image:

```bash
docker build -t energyplus-api .
```

#### Run the Docker Container
Once the image is built, run the container using:

```bash
docker run -p 8080:8080 energyplus-api
```

The API will be accessible at `http://localhost:8080`.

### Pushing the Image to Docker Hub
To share the image via Docker Hub, follow these steps:

1. **Log in to Docker Hub:**
   ```bash
   docker login
   ```
2. **Tag the image:**
   ```bash
   docker tag energyplus-api [DOCKERHUB_USERNAME]/energyplus-api:latest
   ```
3. **Push the image:**
   ```bash
   docker push [DOCKERHUB_USERNAME]/energyplus-api:latest
   ```

## Deploying on Google Cloud

To deploy the Docker image on Google Cloud, follow these steps:

-  **Deploy the container to Cloud Run:**
   ```bash
   gcloud run deploy energyplus-api --image gcr.io/[PROJECT_ID]/energyplus-api --platform managed --region [REGION] --allow-unauthenticated
   ```
-  **Get the API URL:**
   After deployment, Google Cloud will provide a URL for the service.

## Testing the API with Postman

After deployment, use Postman to test the API:

1. **Open Postman** and create a new request.
2. **Set the request type to POST** and enter the API URL followed by `/api/run-simulation`.
3. **Go to the Body tab** and choose `form-data`.
4. **Upload IDF and EPW files** as required.
5. **Send the request** and check the response.

For GET requests, enter the API URL followed by `/api/output-files` and send the request to list output files.

## License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


