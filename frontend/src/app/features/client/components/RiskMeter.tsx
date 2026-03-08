import { Progress } from "./ui/progress";

interface RiskMeterProps {
  score: number;
}

const getRiskColor = (score: number) => {
  if (score <= 3) return "bg-[oklch(0.696_0.17_162.48)]";
  if (score <= 6) return "bg-[oklch(0.769_0.188_70.08)]";
  return "bg-[oklch(0.645_0.246_16.439)]";
};

const getRiskLabel = (score: number) => {
  if (score <= 3) return "Low Risk";
  if (score <= 6) return "Medium Risk";
  return "High Risk";
};

export default function RiskMeter({ score }: RiskMeterProps) {
  const colorClass = getRiskColor(score);
  const label = getRiskLabel(score);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm text-[oklch(0.708_0_0)]">Virality Risk</span>
        <span className={`text-sm font-medium ${colorClass.replace('bg-', 'text-')}`}>
          {label}
        </span>
      </div>
      <div className="relative">
        <div className="h-2 bg-[oklch(0.269_0_0)] rounded-full overflow-hidden">
          <div
            className={`h-full ${colorClass} transition-all duration-500`}
            style={{ width: `${(score / 10) * 100}%` }}
          />
        </div>
      </div>
      <div className="flex items-center justify-between text-xs text-[oklch(0.708_0_0)]">
        <span>1</span>
        <span className="font-medium text-white">{score}/10</span>
        <span>10</span>
      </div>
    </div>
  );
}
