from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

AWS_PRICING_API = 'https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/index.json'
GCP_PRICING_API = 'https://cloudbilling.googleapis.com/v1/services/-/skus'
AZURE_PRICING_API = 'https://prices.azure.com/api/retail/prices'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.json

    num_pods = int(data['numPods'])
    num_replicas = int(data['numReplicas'])
    cpu_per_pod = int(data['cpuPerPod'])
    memory_per_pod = int(data['memoryPerPod'])

    total_cpu = num_pods * num_replicas * cpu_per_pod
    total_memory = num_pods * num_replicas * memory_per_pod

    aws_result = get_aws_pricing(total_cpu, total_memory)
    gcp_result = get_gcp_pricing(total_cpu, total_memory)
    azure_result = get_azure_pricing(total_cpu, total_memory)

    results = [r for r in [aws_result, gcp_result, azure_result] if r]
    best_option = min(results, key=lambda x: x['totalCost'])

    return jsonify(best_option)

def get_aws_pricing(cpu, memory):
    response = requests.get(AWS_PRICING_API)
    data = response.json()
    # Implement the logic to parse the AWS pricing data
    return {
        'provider': 'AWS',
        'instanceType': 't2.micro',
        'totalCost': 100  # Dummy value
    }

def get_gcp_pricing(cpu, memory):
    response = requests.get(GCP_PRICING_API)
    data = response.json()
    # Implement the logic to parse the GCP pricing data
    return {
        'provider': 'GCP',
        'instanceType': 'n1-standard-1',
        'totalCost': 120  # Dummy value
    }

def get_azure_pricing(cpu, memory):
    response = requests.get(AZURE_PRICING_API)
    data = response.json()
    # Implement the logic to parse the Azure pricing data
    return {
        'provider': 'Azure',
        'instanceType': 'B1s',
        'totalCost': 110  # Dummy value
    }

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

