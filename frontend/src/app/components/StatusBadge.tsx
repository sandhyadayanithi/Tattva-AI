interface StatusBadgeProps {
  status: "Pending" | "Reviewing" | "Resolved";
}

const statusStyles = {
  Pending: "bg-[oklch(0.769_0.188_70.08)]/20 text-[oklch(0.769_0.188_70.08)] border-[oklch(0.769_0.188_70.08)]/30",
  Reviewing: "bg-[oklch(0.488_0.243_264.376)]/20 text-[oklch(0.488_0.243_264.376)] border-[oklch(0.488_0.243_264.376)]/30",
  Resolved: "bg-[oklch(0.696_0.17_162.48)]/20 text-[oklch(0.696_0.17_162.48)] border-[oklch(0.696_0.17_162.48)]/30",
};

export default function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <span
      className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-medium border ${statusStyles[status]}`}
    >
      {status}
    </span>
  );
}
