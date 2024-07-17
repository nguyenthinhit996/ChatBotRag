// src/api.js

import axios from "axios";

// const API_BASE_URL = 'http://127.0.0.1:8080/api/'; // Replace with your API base URL
// const API_BASE_URL = 'http://192.168.18.23:8080/api/'; // Replace with your API base URL

const API_BASE_URL = import.meta.env.VITE_API_URL;

const axiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 10 seconds timeout
  headers: {
    "Content-Type": "application/json",
    // Add any headers if needed
  },
});

// Function to handle errors
const handleErrors = (error) => {
  console.error("API Error:", error);
  throw error; // Throw the error further
};

// Function to perform GET request with parameters
export const getData = async (url, params) => {
  try {
    const response = await axiosInstance.get(url, { params });
    return response.data;
  } catch (error) {
    handleErrors(error);
  }
};

// Function to perform POST request with parameters
export const postData = async (url, data, params) => {
  try {
    const response = await axiosInstance.post(url, data, { params });
    return response.data;
  } catch (error) {
    handleErrors(error);
  }
};

// Function to perform PUT request with parameters
export const putData = async (url, data, params) => {
  try {
    const response = await axiosInstance.put(url, data, { params });
    return response.data;
  } catch (error) {
    handleErrors(error);
  }
};

// Function to perform DELETE request with parameters
export const deleteData = async (url, params) => {
  try {
    const response = await axiosInstance.delete(url, { params });
    return response.data;
  } catch (error) {
    handleErrors(error);
  }
};
