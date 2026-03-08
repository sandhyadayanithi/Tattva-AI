import { TrendingUp, TrendingDown } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  suffix?: string;
  trend: number;
  sparklineData: number[];
}

export default function MetricCard({
  title,
  value,
  suffix,
  trend,
  sparklineData,
}: MetricCardProps) {
  const isPositive = trend >= 0;

  return (
    <div className="bg-neutral-900 border border-neutral-800 rounded-xl p-6 hover:border-neutral-700 transition-colors">
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="text-sm text-neutral-400 mb-1">{title}</p>
          <div className="flex items-baseline gap-1">
            <p className="text-3xl font-semibold">{value}</p>
            {suffix && <span className="text-lg text-neutral-500">{suffix}</span>}
          </div>
        </div>
        <div
          className={`flex items-center gap-1 px-2 py-1 rounded-lg ${isPositive ? "bg-green-950 text-green-400" : "bg-red-950 text-red-400"
            }`}
        >
          {isPositive ? (
            <TrendingUp className="w-4 h-4" />
          ) : (
            <TrendingDown className="w-4 h-4" />
          )}
          <span className="text-sm font-medium">{Math.abs(trend)}%</span>
        </div>
      </div>

      <div className="flex items-end gap-1 h-8">
        {sparklineData.map((val, index) => {
          const maxValue = Math.max(...sparklineData);
          const height = (val / maxValue) * 100;
          return (
            <div
              key={index}
              className={`flex-1 rounded-t ${isPositive ? "bg-green-600" : "bg-blue-600"
                }`}
              style={{ height: `${height}%` }}
            />
          );
        })}
      </div>
    </div>
  );
}
