import React from 'react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

export interface ChartData {
  type: string;
  title: string;
  data: Array<Record<string, unknown>>;
  xAxisKey?: string;
  yAxisKey?: string;
  dataKeys?: Array<{ key: string; name: string; color: string }>;
}

export interface InventoryResultsChartProps {
  charts: ChartData[];
}

const COLORS = [
  '#6366f1', // Indigo
  '#8b5cf6', // Purple
  '#ec4899', // Pink
  '#f59e0b', // Amber
  '#10b981', // Emerald
  '#06b6d4', // Cyan
  '#3b82f6', // Blue
  '#ef4444', // Red
  '#14b8a6', // Teal
  '#f97316', // Orange
];

const CustomTooltip = ({ active, payload, label }: any) => {
  if (active && payload && payload.length) {
    return (
      <div
        style={{
          backgroundColor: 'white',
          padding: '12px',
          border: '1px solid #e2e8f0',
          borderRadius: '8px',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
        }}
      >
        <p style={{ marginBottom: '8px', fontWeight: 600, color: '#1e293b' }}>
          {label}
        </p>
        {payload.map((entry: any, index: number) => (
          <p
            key={index}
            style={{
              color: entry.color,
              margin: '4px 0',
              fontSize: '14px',
            }}
          >
            <span style={{ fontWeight: 600 }}>{entry.name}:</span>{' '}
            {typeof entry.value === 'number'
              ? entry.value.toLocaleString()
              : entry.value}
          </p>
        ))}
      </div>
    );
  }
  return null;
};

const formatNumber = (value: number): string => {
  if (value >= 1000000) {
    return `${(value / 1000000).toFixed(1)}M`;
  }
  if (value >= 1000) {
    return `${(value / 1000).toFixed(1)}K`;
  }
  return value.toString();
};

export const InventoryResultsChart: React.FC<InventoryResultsChartProps> = ({
  charts,
}) => {
  if (charts.length === 0) {
    return (
      <div className="results-chart empty">
        <p>No chart data available</p>
      </div>
    );
  }

  const renderChart = (chart: ChartData, index: number) => {
    const xAxisKey = chart.xAxisKey || 'name';
    const dataKeys = chart.dataKeys || [
      { key: 'value', name: 'Value', color: COLORS[0] },
    ];

    // Calculate statistics
    const stats = dataKeys.map((dk) => {
      const values = chart.data
        .map((d) => d[dk.key] as number)
        .filter((v) => typeof v === 'number');
      const sum = values.reduce((a, b) => a + b, 0);
      const avg = values.length > 0 ? sum / values.length : 0;
      const max = values.length > 0 ? Math.max(...values) : 0;
      return { key: dk.key, name: dk.name, sum, avg, max, count: values.length };
    });

    return (
      <div key={index} className="chart-container">
        <h3>{chart.title}</h3>
        
        {/* Statistics */}
        <div className="chart-stats">
          {stats.map((stat, statIndex) => (
            <div key={statIndex} className="chart-stat">
              <div className="chart-stat-label">{stat.name} - Total</div>
              <div className="chart-stat-value">{formatNumber(stat.sum)}</div>
            </div>
          ))}
          {stats[0] && (
            <>
              <div className="chart-stat">
                <div className="chart-stat-label">Average</div>
                <div className="chart-stat-value">
                  {formatNumber(stats[0].avg)}
                </div>
              </div>
              <div className="chart-stat">
                <div className="chart-stat-label">Max</div>
                <div className="chart-stat-value">
                  {formatNumber(stats[0].max)}
                </div>
              </div>
              <div className="chart-stat">
                <div className="chart-stat-label">Items</div>
                <div className="chart-stat-value">{stats[0].count}</div>
              </div>
            </>
          )}
        </div>

        <ResponsiveContainer width="100%" height={400}>
          {chart.type === 'line' ? (
            <LineChart data={chart.data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis
                dataKey={xAxisKey}
                stroke="#64748b"
                style={{ fontSize: '12px' }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis
                stroke="#64748b"
                style={{ fontSize: '12px' }}
                tickFormatter={formatNumber}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend
                wrapperStyle={{ paddingTop: '20px' }}
                iconType="line"
              />
              {dataKeys.map((dk) => (
                <Line
                  key={dk.key}
                  type="monotone"
                  dataKey={dk.key}
                  name={dk.name}
                  stroke={dk.color}
                  strokeWidth={2}
                  dot={{ fill: dk.color, r: 4 }}
                  activeDot={{ r: 6 }}
                />
              ))}
            </LineChart>
          ) : chart.type === 'area' ? (
            <AreaChart data={chart.data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
              <defs>
                {dataKeys.map((dk, dkIndex) => (
                  <linearGradient
                    key={dk.key}
                    id={`color${dkIndex}`}
                    x1="0"
                    y1="0"
                    x2="0"
                    y2="1"
                  >
                    <stop offset="5%" stopColor={dk.color} stopOpacity={0.8} />
                    <stop offset="95%" stopColor={dk.color} stopOpacity={0.1} />
                  </linearGradient>
                ))}
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis
                dataKey={xAxisKey}
                stroke="#64748b"
                style={{ fontSize: '12px' }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis
                stroke="#64748b"
                style={{ fontSize: '12px' }}
                tickFormatter={formatNumber}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              {dataKeys.map((dk, dkIndex) => (
                <Area
                  key={dk.key}
                  type="monotone"
                  dataKey={dk.key}
                  name={dk.name}
                  stroke={dk.color}
                  fill={`url(#color${dkIndex})`}
                  strokeWidth={2}
                />
              ))}
            </AreaChart>
          ) : chart.type === 'pie' ? (
            <PieChart>
              <Pie
                data={chart.data}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }: any) =>
                  `${name}: ${(percent * 100).toFixed(0)}%`
                }
                outerRadius={120}
                fill="#8884d8"
                dataKey={dataKeys[0]?.key || 'value'}
              >
                {chart.data.map((_entry, entryIndex) => (
                  <Cell
                    key={`cell-${entryIndex}`}
                    fill={COLORS[entryIndex % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend />
            </PieChart>
          ) : (
            <BarChart data={chart.data} margin={{ top: 5, right: 20, left: 10, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
              <XAxis
                dataKey={xAxisKey}
                stroke="#64748b"
                style={{ fontSize: '12px' }}
                angle={-45}
                textAnchor="end"
                height={80}
              />
              <YAxis
                stroke="#64748b"
                style={{ fontSize: '12px' }}
                tickFormatter={formatNumber}
              />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ paddingTop: '20px' }} />
              {dataKeys.map((dk, dkIndex) => (
                <Bar
                  key={dk.key}
                  dataKey={dk.key}
                  name={dk.name}
                  fill={dk.color}
                  radius={[8, 8, 0, 0]}
                />
              ))}
            </BarChart>
          )}
        </ResponsiveContainer>
      </div>
    );
  };

  return <div className="results-chart">{charts.map(renderChart)}</div>;
};

