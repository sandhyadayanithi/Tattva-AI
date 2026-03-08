import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "../../shared/components/ui/card";
import { mockClaims } from "../../shared/data/mockData";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "../../shared/components/ui/tabs";
import { Languages } from "lucide-react";

const languageTranslations: Record<string, Record<string, string>> = {
  "FC-2026-001": {
    english: "This claim is false. The government has not made any such announcement. The viral message appears to be a misinterpretation of a subsidy program for low-income households consuming less than 100 units per month.",
    tamil: "இந்தக் கூற்று தவறானது. அரசு அத்தகைய அறிவிப்பை வெளியிடவில்லை. வைரல் செய்தி மாதத்திற்கு 100 யூனிட்டுக்கும் குறைவாக பயன்படுத்தும் குறைந்த வருமானம் கொண்ட குடும்பங்களுக்கான மானியத் திட்டத்தை தவறாகப் புரிந்துகொண்டதாகத் தெரிகிறது.",
    hindi: "यह दावा गलत है। सरकार ने ऐसी कोई घोषणा नहीं की है। वायरल संदेश प्रति माह 100 यूनिट से कम खपत करने वाले कम आय वाले परिवारों के लिए सब्सिडी कार्यक्रम की गलत व्याख्या प्रतीत होता है।",
    telugu: "ఈ వాదన తప్పు. ప్రభుత్వం అలాంటి ప్రకటన చేయలేదు. వైరల్ సందేశం నెలకు 100 యూనిట్ల కంటే తక్కువ వినియోగించే తక్కువ ఆదాయ కుటుంబాలకు సబ్సిడీ కార్యక్రమానికి తప్పుడు అర్థం వచ్చినట్లు కనిపిస్తోంది.",
    bengali: "এই দাবিটি মিথ্যা। সরকার এই ধরনের কোনো ঘোষণা করেনি। ভাইরাল বার্তাটি মাসিক 100 ইউনিটের কম ব্যবহারকারী নিম্ন আয়ের পরিবারগুলির জন্য ভর্তুকি প্রোগ্রামের ভুল ব্যাখ্যা বলে মনে হচ্ছে।",
  },
};

export default function LanguageTranslation() {
  const [selectedClaimId, setSelectedClaimId] = useState("FC-2026-001");
  const selectedClaim = mockClaims.find((c) => c.id === selectedClaimId);

  const translations = languageTranslations[selectedClaimId] || {
    english: selectedClaim?.explanation || "",
    tamil: "மொழிபெயர்ப்பு கிடைக்கவில்லை",
    hindi: "अनुवाद उपलब्ध नहीं है",
    telugu: "అనువాదం అందుబాటులో లేదు",
    bengali: "অনুবাদ উপলব্ধ নেই",
  };

  return (
    <div className="space-y-6">
      {/* Claim Selector */}
      <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
        <CardHeader>
          <CardTitle className="text-white flex items-center gap-2">
            <Languages size={20} />
            Select Claim for Translation
          </CardTitle>
        </CardHeader>
        <CardContent>
          <select
            value={selectedClaimId}
            onChange={(e) => setSelectedClaimId(e.target.value)}
            className="w-full px-4 py-3 bg-[oklch(0.269_0_0)] border border-[oklch(0.269_0_0)] text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-[oklch(0.488_0.243_264.376)]"
          >
            {mockClaims.map((claim) => (
              <option key={claim.id} value={claim.id}>
                {claim.id} - {claim.claimSummary}
              </option>
            ))}
          </select>
        </CardContent>
      </Card>

      {selectedClaim && (
        <>
          {/* Original Transcript */}
          <div className="grid grid-cols-2 gap-6">
            <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
              <CardHeader>
                <CardTitle className="text-white">Original Transcript</CardTitle>
                <p className="text-sm text-[oklch(0.708_0_0)]">Language: {selectedClaim.language}</p>
              </CardHeader>
              <CardContent>
                <div className="p-4 bg-[oklch(0.269_0_0)] rounded-lg">
                  <p className="text-white leading-relaxed">{selectedClaim.originalTranscript}</p>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
              <CardHeader>
                <CardTitle className="text-white">English Translation</CardTitle>
                <p className="text-sm text-[oklch(0.708_0_0)]">Translated Version</p>
              </CardHeader>
              <CardContent>
                <div className="p-4 bg-[oklch(0.269_0_0)] rounded-lg">
                  <p className="text-white leading-relaxed">{selectedClaim.translatedClaim}</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Multi-Language Explanation */}
          <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
            <CardHeader>
              <CardTitle className="text-white">Fact Check Explanation - Multi-Language</CardTitle>
              <p className="text-sm text-[oklch(0.708_0_0)]">
                View the explanation in different languages
              </p>
            </CardHeader>
            <CardContent>
              <Tabs defaultValue="english" className="w-full">
                <TabsList className="grid w-full grid-cols-5 bg-[oklch(0.269_0_0)]">
                  <TabsTrigger value="english" className="data-[state=active]:bg-[oklch(0.488_0.243_264.376)] data-[state=active]:text-white">
                    English
                  </TabsTrigger>
                  <TabsTrigger value="tamil" className="data-[state=active]:bg-[oklch(0.488_0.243_264.376)] data-[state=active]:text-white">
                    Tamil
                  </TabsTrigger>
                  <TabsTrigger value="hindi" className="data-[state=active]:bg-[oklch(0.488_0.243_264.376)] data-[state=active]:text-white">
                    Hindi
                  </TabsTrigger>
                  <TabsTrigger value="telugu" className="data-[state=active]:bg-[oklch(0.488_0.243_264.376)] data-[state=active]:text-white">
                    Telugu
                  </TabsTrigger>
                  <TabsTrigger value="bengali" className="data-[state=active]:bg-[oklch(0.488_0.243_264.376)] data-[state=active]:text-white">
                    Bengali
                  </TabsTrigger>
                </TabsList>

                <TabsContent value="english" className="mt-6">
                  <div className="p-6 bg-[oklch(0.269_0_0)] rounded-lg">
                    <p className="text-white leading-relaxed">{translations.english}</p>
                  </div>
                </TabsContent>

                <TabsContent value="tamil" className="mt-6">
                  <div className="p-6 bg-[oklch(0.269_0_0)] rounded-lg">
                    <p className="text-white leading-relaxed">{translations.tamil}</p>
                  </div>
                </TabsContent>

                <TabsContent value="hindi" className="mt-6">
                  <div className="p-6 bg-[oklch(0.269_0_0)] rounded-lg">
                    <p className="text-white leading-relaxed">{translations.hindi}</p>
                  </div>
                </TabsContent>

                <TabsContent value="telugu" className="mt-6">
                  <div className="p-6 bg-[oklch(0.269_0_0)] rounded-lg">
                    <p className="text-white leading-relaxed">{translations.telugu}</p>
                  </div>
                </TabsContent>

                <TabsContent value="bengali" className="mt-6">
                  <div className="p-6 bg-[oklch(0.269_0_0)] rounded-lg">
                    <p className="text-white leading-relaxed">{translations.bengali}</p>
                  </div>
                </TabsContent>
              </Tabs>
            </CardContent>
          </Card>

          {/* Language Stats */}
          <div className="grid grid-cols-3 gap-6">
            <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
              <CardHeader>
                <CardTitle className="text-sm text-[oklch(0.708_0_0)]">Original Language</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-semibold text-white">{selectedClaim.language}</p>
              </CardContent>
            </Card>

            <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
              <CardHeader>
                <CardTitle className="text-sm text-[oklch(0.708_0_0)]">Available Translations</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-semibold text-white">5 Languages</p>
              </CardContent>
            </Card>

            <Card className="bg-[oklch(0.205_0_0)] border-[oklch(0.269_0_0)]">
              <CardHeader>
                <CardTitle className="text-sm text-[oklch(0.708_0_0)]">Translation Accuracy</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-2xl font-semibold text-white">94%</p>
              </CardContent>
            </Card>
          </div>
        </>
      )}
    </div>
  );
}
