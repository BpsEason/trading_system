import axios from 'axios';
const API = axios.create({ baseURL: 'http://localhost:8000/api' }); // 指向 Django 服務
export const fetchOrders = () => API.get('/orders/');
# TODO: 可以添加更多 API 請求，例如創建訂單、更新訂單等
