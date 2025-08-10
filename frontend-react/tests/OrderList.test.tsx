import { render, screen } from '@testing-library/react';
import React from 'react';
import OrderList from '../src/components/OrderList';

test('renders Orders header', () => {
  render(<div><h1>Orders</h1><OrderList/></div>);
  expect(screen.getByText(/Orders/i)).toBeInTheDocument();
});
