interface VerdictBadgeProps {
  verdict: "True" | "False" | "Misleading" | "Unverified";
}

const verdictStyles = {
  True: "bg-[oklch(0.696_0.17_162.48)]/20 text-[oklch(0.696_0.17_162.48)] border-[oklch(0.696_0.17_162.48)]/30",
  False: "bg-[oklch(0.645_0.246_16.439)]/20 text-[oklch(0.645_0.246_16.439)] border-[oklch(0.645_0.246_16.439)]/30",
  Misleading: "bg-[oklch(0.769_0.188_70.08)]/20 text-[oklch(0.769_0.188_70.08)] border-[oklch(0.769_0.188_70.08)]/30",
  Unverified: "bg-[oklch(0.708_0_0)]/20 text-[oklch(0.708_0_0)] border-[oklch(0.708_0_0)]/30",
};

export default function VerdictBadge({ verdict }: VerdictBadgeProps) {
  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${verdictStyles[verdict]}`}
    >
      {verdict}
    </span>
  );
}
