import { Badge } from "../ui/badge";

interface LanguageTagsProps {
  languages: string[];
}

const languageColors: Record<string, string> = {
  Tamil: "bg-blue-100 dark:bg-blue-950 text-blue-700 dark:text-blue-400",
  Hindi: "bg-purple-100 dark:bg-purple-950 text-purple-700 dark:text-purple-400",
  Telugu: "bg-pink-100 dark:bg-pink-950 text-pink-700 dark:text-pink-400",
  Bengali: "bg-orange-100 dark:bg-orange-950 text-orange-700 dark:text-orange-400",
};

export function LanguageTags({ languages }: LanguageTagsProps) {
  return (
    <div className="flex flex-wrap gap-1">
      {languages.map((lang) => (
        <Badge
          key={lang}
          variant="secondary"
          className={languageColors[lang] || ""}
        >
          {lang}
        </Badge>
      ))}
    </div>
  );
}
