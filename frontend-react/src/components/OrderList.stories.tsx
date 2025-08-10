import type { Meta, StoryObj } from '@storybook/react';
import OrderList from './OrderList';

const meta: Meta<typeof OrderList> = {
  title: 'Components/OrderList',
  component: OrderList,
  tags: ['autodocs'],
  parameters: {
    layout: 'centered',
  },
};

export default meta;
type Story = StoryObj<typeof OrderList>;

export const Default: Story = {
  args: {},
};
