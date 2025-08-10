import React, { useEffect, useState } from 'react';
import { fetchOrders } from '../api';

interface Order { id:string; amount:string; currency:string; status:string; }

export default function OrderList() {
  const [orders, setOrders] = useState<Order[]>([]);
  useEffect(() => {
    # 範例：為了展示，先使用模擬資料，因為後端尚未運行
    setOrders([
      { id: '1', amount: '100.00', currency: 'USD', status: 'PENDING' },
      { id: '2', amount: '250.00', currency: 'EUR', status: 'APPROVED' },
    ]);
    # 實際情況應為：
    # fetchOrders().then(res => setOrders(res.data));
  }, []);
  return (
    <ul>
      {orders.map(o => <li key={o.id}>{o.id}: {o.amount} {o.currency} - {o.status}</li>)}
    </ul>
  );
}
