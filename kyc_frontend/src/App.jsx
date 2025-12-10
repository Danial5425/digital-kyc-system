import { useState } from "react";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

function App() {
  const [aadhaar, setAadhaar] = useState("");
  const [pan, setPan] = useState("");
  const [passport, setPassport] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await axios.post(`${API_BASE}/kyc/submit`, {
        aadhaar: aadhaar.trim(),
        pan: pan.trim().toUpperCase(),
        passport: passport.trim().toUpperCase(),
      });
      setResult(response.data);
    } catch (err) {
      console.error(err);
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  const statusBadge = (doc) => {
    const base =
      "inline-flex px-2 py-1 rounded-full text-xs font-semibold";
    if (!doc.is_valid)
      return (
        <span className={`${base} bg-red-100 text-red-700`}>Rejected</span>
      );
    return (
      <span className={`${base} bg-emerald-100 text-emerald-700`}>
        Valid
      </span>
    );
  };

  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-lg p-8 border border-slate-100">
        {/* Header */}
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-lg bg-hdfcBlue flex items-center justify-center text-white font-bold">
              K
            </div>
            <div>
              <h1 className="text-xl font-semibold text-hdfcBlue">
                Digital KYC Verification
              </h1>
              <p className="text-xs text-slate-500">
                Demo backend: checksum + duplicate detection (no govt APIs).
              </p>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full text-xs bg-hdfcRed text-white font-semibold">
            HDFC Demo
          </span>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          <div className="flex flex-col">
            <label className="text-xs font-medium text-slate-600 mb-1">
              Aadhaar Number
            </label>
            <input
              type="text"
              value={aadhaar}
              onChange={(e) => setAadhaar(e.target.value)}
              className="border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-hdfcBlue focus:border-transparent"
              placeholder="12-digit Aadhaar"
              autoComplete="off"
            />
          </div>
          <div className="flex flex-col">
            <label className="text-xs font-medium text-slate-600 mb-1">
              PAN
            </label>
            <input
              type="text"
              value={pan}
              onChange={(e) => setPan(e.target.value)}
              className="border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-hdfcBlue focus:border-transparent uppercase"
              placeholder="ABCDE1234Z"
              autoComplete="off"
            />
          </div>
          <div className="flex flex-col">
            <label className="text-xs font-medium text-slate-600 mb-1">
              Passport
            </label>
            <input
              type="text"
              value={passport}
              onChange={(e) => setPassport(e.target.value)}
              className="border border-slate-200 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-hdfcBlue focus:border-transparent uppercase"
              placeholder="X1234567"
              autoComplete="off"
            />
          </div>
        </form>

        {/* Submit + state */}
        <div className="flex items-center justify-between mb-3">
          <button
            onClick={handleSubmit}
            disabled={loading}
            className="px-4 py-2 rounded-lg bg-hdfcBlue text-white text-sm font-semibold hover:bg-blue-900 disabled:opacity-60"
          >
            {loading ? "Validating..." : "Submit KYC"}
          </button>
          {result && (
            <span
              className={`text-xs font-semibold px-3 py-1 rounded-full ${
                result.overall_status === "approved"
                  ? "bg-emerald-100 text-emerald-700"
                  : "bg-red-100 text-red-700"
              }`}
            >
              Overall: {result.overall_status.toUpperCase()}
            </span>
          )}
        </div>

        {/* Error */}
        {error && (
          <div className="mb-3 text-xs text-red-600 bg-red-50 border border-red-100 rounded-lg px-3 py-2">
            {error}
          </div>
        )}

        {/* Result */}
        {result && (
          <div className="mt-4 border border-slate-100 rounded-xl p-4 bg-slate-50">
            <h2 className="text-sm font-semibold text-slate-700 mb-2">
              Document Status
            </h2>
            <div className="space-y-2">
              {result.documents.map((doc) => (
                <div
                  key={doc.document_type}
                  className="flex items-center justify-between bg-white rounded-lg px-3 py-2 border border-slate-100"
                >
                  <div>
                    <div className="text-xs font-semibold uppercase text-slate-600">
                      {doc.document_type}
                    </div>
                    <div className="text-xs text-slate-500">
                      {doc.value || "-"}
                    </div>
                    <div className="text-[11px] text-slate-500 mt-0.5">
                      {doc.reason}
                    </div>
                  </div>
                  {statusBadge(doc)}
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
