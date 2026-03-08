export interface Claim {
  id: string;
  claimSummary: string;
  verdict: "True" | "False" | "Misleading" | "Unverified";
  language: string;
  confidence: number;
  viralityRisk: number;
  dateChecked: string;
  originalTranscript: string;
  translatedClaim: string;
  explanation: string;
}

export interface DiscrepancyReport {
  id: string;
  claimId: string;
  issueType: string;
  submittedDate: string;
  status: "Pending" | "Reviewing" | "Resolved";
  explanation: string;
}

export const mockClaims: Claim[] = [
  {
    id: "FC-2026-001",
    claimSummary: "Government announced free electricity for all households",
    verdict: "False",
    language: "Tamil",
    confidence: 87,
    viralityRisk: 8,
    dateChecked: "2026-03-05",
    originalTranscript: "அரசு அனைத்து வீடுகளுக்கும் இலவச மின்சாரம் வழங்குவதாக அறிவித்துள்ளது",
    translatedClaim: "Government announced free electricity for all households",
    explanation: "This claim is false. The government has not made any such announcement. The viral message appears to be a misinterpretation of a subsidy program for low-income households consuming less than 100 units per month. Official government press releases and statements from the Ministry of Power confirm that there is no universal free electricity scheme."
  },
  {
    id: "FC-2026-002",
    claimSummary: "New vaccine causes severe side effects in children",
    verdict: "Misleading",
    language: "Hindi",
    confidence: 92,
    viralityRisk: 9,
    dateChecked: "2026-03-04",
    originalTranscript: "नई वैक्सीन से बच्चों में गंभीर दुष्प्रभाव हो रहे हैं",
    translatedClaim: "New vaccine causes severe side effects in children",
    explanation: "This claim is misleading. While all vaccines can have side effects, the rate of severe side effects from this vaccine is extremely low (0.001%). The claim exaggerates isolated incidents and lacks context about the overall safety profile. Clinical trials involving 50,000 children showed the vaccine to be safe and effective. Health authorities continue to recommend it."
  },
  {
    id: "FC-2026-003",
    claimSummary: "Rice contains plastic particles from China",
    verdict: "False",
    language: "Telugu",
    confidence: 95,
    viralityRisk: 7,
    dateChecked: "2026-03-03",
    originalTranscript: "చైనా నుండి వచ్చిన బియ్యంలో ప్లాస్టిక్ కణాలు ఉన్నాయి",
    translatedClaim: "Rice contains plastic particles from China",
    explanation: "This is a false claim that has been repeatedly debunked. Laboratory tests conducted by food safety authorities found no evidence of plastic in rice samples. The viral videos showing 'plastic rice' actually demonstrate normal rice behavior when exposed to heat. This is a recurring hoax that surfaces periodically across different regions."
  },
  {
    id: "FC-2026-004",
    claimSummary: "WhatsApp will start charging monthly fees",
    verdict: "False",
    language: "Bengali",
    confidence: 98,
    viralityRisk: 6,
    dateChecked: "2026-03-02",
    originalTranscript: "হোয়াটসঅ্যাপ মাসিক ফি নেওয়া শুরু করবে",
    translatedClaim: "WhatsApp will start charging monthly fees",
    explanation: "This claim is completely false. WhatsApp has officially stated that the service will remain free for all users. This hoax has been circulating in various forms since 2016. WhatsApp generates revenue through its business API and has no plans to charge individual users. The company has repeatedly debunked this rumor on its official channels."
  },
  {
    id: "FC-2026-005",
    claimSummary: "Drinking hot water prevents COVID-19",
    verdict: "False",
    language: "Hindi",
    confidence: 100,
    viralityRisk: 5,
    dateChecked: "2026-03-01",
    originalTranscript: "गर्म पानी पीने से कोविड-19 से बचा जा सकता है",
    translatedClaim: "Drinking hot water prevents COVID-19",
    explanation: "This claim is false. There is no scientific evidence that drinking hot water prevents COVID-19 infection. The virus is transmitted through respiratory droplets and contact with contaminated surfaces. While staying hydrated is important for overall health, hot water does not kill the virus or prevent infection. WHO and CDC guidelines do not include hot water consumption as a preventive measure."
  },
  {
    id: "FC-2026-006",
    claimSummary: "Solar eclipse causes harmful radiation",
    verdict: "Misleading",
    language: "Tamil",
    confidence: 85,
    viralityRisk: 4,
    dateChecked: "2026-02-28",
    originalTranscript: "சூரிய கிரகணம் தீங்கு விளைவிக்கும் கதிர்வீச்சை ஏற்படுத்துகிறது",
    translatedClaim: "Solar eclipse causes harmful radiation",
    explanation: "This claim is misleading. Solar eclipses do not produce any special or additional harmful radiation. The danger comes from looking directly at the sun during a partial eclipse without proper eye protection, which can damage the retina. The sun emits the same radiation during an eclipse as it does normally. There is no need to stay indoors or take special precautions beyond not looking directly at the sun."
  }
];

export const mockReports: DiscrepancyReport[] = [
  {
    id: "DR-001",
    claimId: "FC-2026-001",
    issueType: "Incorrect verdict",
    submittedDate: "2026-03-06",
    status: "Pending",
    explanation: "The verdict seems too harsh. There was a subsidy announcement that could be misinterpreted."
  },
  {
    id: "DR-002",
    claimId: "FC-2026-003",
    issueType: "Missing evidence",
    submittedDate: "2026-03-05",
    status: "Reviewing",
    explanation: "Please provide links to the laboratory test reports mentioned in the explanation."
  },
  {
    id: "DR-003",
    claimId: "FC-2026-002",
    issueType: "Incorrect transcript",
    submittedDate: "2026-03-04",
    status: "Resolved",
    explanation: "The Hindi transcript contains a minor spelling error in the original text."
  }
];
