const { initializeApp } = require("firebase-admin/app");
const { getFirestore } = require("firebase-admin/firestore");
const { getStorage } = require("firebase-admin/storage");
const { onCall, onRequest, HttpsError } = require("firebase-functions/v2/https");
const { setGlobalOptions } = require("firebase-functions/v2");

setGlobalOptions({ region: "us-central1" });
initializeApp();

const db = getFirestore();
const storage = getStorage();
const defaultBucket = storage.bucket();

exports.myGeminiFunction = onRequest(async (req, res) => {
  const GEMINI_API_KEY = process.env.GEMINI_API_KEY;
  if (!GEMINI_API_KEY) {
    res.status(500).send("Gemini API Key is not configured.");
    return;
  }
  res.send("Function is ready to use Gemini!");
});

const carPartsList = [
  "Car body", "Body trim", "Interior cab", "Engine compartment", "Bonnet/hood",
  "Bonnet support stick", "Bonnet hinges and springs", "Car cover", "Bumper", "Unexposed bumper",
  "Exposed bumper", "Cowl screen", "Decklid", "Fender", "Fascia", "Grille", "Pillar",
  "Quarter panel", "Radiator core support", "Rocker panel", "Roof rack", "Spoiler",
  "Front spoiler", "Rear spoiler", "Rims", "Hubcap", "Tire", "Trim package", "Trunk/boot",
  "Trunk latch", "Valance", "Welded assembly", "Anti-intrusion bar", "Outer door handle",
  "Inner door handle", "Door control module", "Door seal", "Door water-shield", "Door hinge",
  "Door latch", "Door lock", "Central locking system", "Fuel tank door", "Window glass",
  "Sunroof", "Sunroof motor", "Sunroof rail", "Window motor", "Window regulator", "Windshield",
  "Windshield washer motor", "Window seal", "Radio and media player", "Speaker",
  "Antenna assembly", "Backup camera", "Dashcam", "Alternator", "Battery", "Voltage regulator",
  "Fuel gauge", "Odometer", "Speedometer", "Tachometer", "Temperature gauge", "Ignition system",
  "Distributor", "Ignition coil", "Spark plug", "Glow plug", "Headlight", "Tail light",
  "Brake light", "Turn signal", "ABS sensor", "Airbag sensor", "Crankshaft position sensor",
  "Oxygen sensor", "Starter motor", "Starter solenoid", "Ignition switch", "Wiring harness",
  "Engine control unit (ECU)", "Fuse box", "Carpet", "Center console", "Roll cage",
  "Dashboard", "Car seat", "Armrest", "Headrest", "Seat belt", "Brake disc", "Brake pad",
  "Brake caliper", "Master cylinder", "Brake booster", "Electric motor", "High voltage battery pack",
  "Battery management system (BMS)", "Fuel cell", "Inverter", "Charge port", "Engine block",
  "Crankshaft", "Piston", "Cylinder head", "Camshaft", "Timing belt", "Turbocharger",
  "Supercharger", "Radiator", "Cooling fan", "Water pump", "Oil filter", "Oil pan",
  "Exhaust manifold", "Catalytic converter", "Muffler", "Fuel tank", "Fuel pump",
  "Fuel injector", "Air filter", "Throttle body", "Axle", "Control arm", "Shock absorber",
  "Coil spring", "Steering rack", "Power steering pump", "Steering wheel", "Tie rod end",
  "Clutch", "Gearbox", "Driveshaft", "Differential", "Air conditioning compressor",
  "Air conditioning condenser", "Cabin air filter", "Wheel bearing", "Horn", "Airbag", "Sun visor"
];

exports.buildPartsDatabase = onCall(async (request) => {
  console.log("Starting to build parts database...");
  const [exists] = await defaultBucket.exists();
  if (!exists) {
    const errorMessage = "Default Cloud Storage bucket not found. Please create one.";
    console.error(errorMessage);
    throw new HttpsError('failed-precondition', errorMessage);
  }
  console.log(`Verified default bucket exists: ${defaultBucket.name}`);

  for (const partName of carPartsList) {
    try {
      console.log(`Processing part: ${partName}`);
      const placeholderImageUrl = `https://placehold.co/600x400/0d1117/3B82F6?text=${encodeURIComponent(partName)}`;
      const fetchRes = await fetch(placeholderImageUrl);
      if (!fetchRes.ok) {
        throw new Error(`Failed to fetch placeholder image for ${partName}`);
      }
      const arrayBuffer = await fetchRes.arrayBuffer();
      const buffer = Buffer.from(arrayBuffer);
      const fileName = `${partName.replace(/[\s\/]/g, '_')}.png`;
      const filePath = `part-images/${fileName}`;
      const file = defaultBucket.file(filePath);
      await file.save(buffer, { metadata: { contentType: 'image/png' } });
      const [publicUrl] = await file.getSignedUrl({ action: 'read', expires: '03-09-2491' });
      const partRef = db.collection('parts').doc(partName.toLowerCase().replace(/\s/g, '-'));
      await partRef.set({ partName: partName, imageUrl: publicUrl, createdAt: new Date() });
      console.log(`Saved "${partName}" to Firestore.`);
    } catch (error) {
      console.error(`Failed to process part: ${partName}`, error);
    }
  }
  const successMessage = "Successfully finished building the parts database.";
  console.log(successMessage);
  return { status: "success", message: successMessage };
});
