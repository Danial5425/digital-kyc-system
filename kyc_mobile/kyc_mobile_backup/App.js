import React, { useState } from "react";
import { SafeAreaView, View, Text, TextInput, TouchableOpacity, ActivityIndicator, ScrollView } from "react-native";
import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export default function App() {
  const [aadhaar, setAadhaar] = useState("");
  const [pan, setPan] = useState("");
  const [passport, setPassport] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const submitKYC = async () => {
    setLoading(true);
    setResult(null);
    setError("");

    try {
      const res = await axios.post(`${API_BASE}/kyc/submit`, {
        aadhaar: aadhaar.trim(),
        pan: pan.trim().toUpperCase(),
        passport: passport.trim().toUpperCase(),
      });
      setResult(res.data);
    } catch (e) {
      console.log(e);
      setError("Network or server error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: "#F3F6FA" }}>
      <ScrollView contentContainerStyle={{ flexGrow: 1, padding: 16 }}>
        <View
          style={{
            backgroundColor: "#ffffff",
            borderRadius: 16,
            padding: 16,
            shadowColor: "#000",
            shadowOpacity: 0.05,
            shadowRadius: 8,
            elevation: 3,
          }}
        >
          <View
            style={{
              flexDirection: "row",
              justifyContent: "space-between",
              marginBottom: 12,
              alignItems: "center",
            }}
          >
            <View style={{ flexDirection: "row", alignItems: "center" }}>
              <View
                style={{
                  width: 32,
                  height: 32,
                  borderRadius: 8,
                  backgroundColor: "#004C8F",
                  alignItems: "center",
                  justifyContent: "center",
                  marginRight: 8,
                }}
              >
                <Text style={{ color: "#fff", fontWeight: "700" }}>K</Text>
              </View>
              <View>
                <Text style={{ fontSize: 16, fontWeight: "600", color: "#004C8F" }}>
                  Digital KYC
                </Text>
                <Text style={{ fontSize: 11, color: "#6b7280" }}>
                  HDFC-style checksum & duplicate check
                </Text>
              </View>
            </View>
            <View
              style={{
                paddingHorizontal: 8,
                paddingVertical: 4,
                borderRadius: 999,
                backgroundColor: "#E31837",
              }}
            >
              <Text style={{ color: "#fff", fontSize: 10, fontWeight: "600" }}>
                DEMO
              </Text>
            </View>
          </View>

          {/* Inputs */}
          <View style={{ marginBottom: 8 }}>
            <Text style={{ fontSize: 11, color: "#4b5563", marginBottom: 4 }}>
              Aadhaar
            </Text>
            <TextInput
              value={aadhaar}
              onChangeText={setAadhaar}
              placeholder="12-digit Aadhaar"
              keyboardType="number-pad"
              style={{
                borderWidth: 1,
                borderColor: "#e5e7eb",
                borderRadius: 10,
                paddingHorizontal: 10,
                paddingVertical: 8,
                fontSize: 13,
              }}
            />
          </View>

          <View style={{ marginBottom: 8 }}>
            <Text style={{ fontSize: 11, color: "#4b5563", marginBottom: 4 }}>
              PAN
            </Text>
            <TextInput
              value={pan}
              onChangeText={(t) => setPan(t.toUpperCase())}
              placeholder="ABCDE1234Z"
              autoCapitalize="characters"
              style={{
                borderWidth: 1,
                borderColor: "#e5e7eb",
                borderRadius: 10,
                paddingHorizontal: 10,
                paddingVertical: 8,
                fontSize: 13,
              }}
            />
          </View>

          <View style={{ marginBottom: 12 }}>
            <Text style={{ fontSize: 11, color: "#4b5563", marginBottom: 4 }}>
              Passport
            </Text>
            <TextInput
              value={passport}
              onChangeText={(t) => setPassport(t.toUpperCase())}
              placeholder="X1234567"
              autoCapitalize="characters"
              style={{
                borderWidth: 1,
                borderColor: "#e5e7eb",
                borderRadius: 10,
                paddingHorizontal: 10,
                paddingVertical: 8,
                fontSize: 13,
              }}
            />
          </View>

          {/* Button */}
          <TouchableOpacity
            onPress={submitKYC}
            disabled={loading}
            style={{
              backgroundColor: "#004C8F",
              borderRadius: 999,
              paddingVertical: 10,
              alignItems: "center",
              marginBottom: 8,
              opacity: loading ? 0.6 : 1,
            }}
          >
            {loading ? (
              <ActivityIndicator color="#fff" />
            ) : (
              <Text
                style={{
                  color: "#fff",
                  fontWeight: "600",
                  fontSize: 13,
                }}
              >
                Submit KYC
              </Text>
            )}
          </TouchableOpacity>

          {/* Error */}
          {error ? (
            <Text
              style={{
                fontSize: 11,
                color: "#b91c1c",
                backgroundColor: "#fef2f2",
                borderRadius: 8,
                padding: 8,
                marginBottom: 4,
              }}
            >
              {error}
            </Text>
          ) : null}

          {/* Result */}
          {result && (
            <View
              style={{
                marginTop: 8,
                padding: 10,
                borderRadius: 10,
                backgroundColor: "#f3f4f6",
              }}
            >
              <Text
                style={{
                  fontSize: 12,
                  fontWeight: "600",
                  marginBottom: 6,
                  color:
                    result.overall_status === "approved"
                      ? "#15803d"
                      : "#b91c1c",
                }}
              >
                Overall: {result.overall_status.toUpperCase()}
              </Text>

              {result.documents.map((doc) => (
                <View
                  key={doc.document_type}
                  style={{
                    backgroundColor: "#fff",
                    borderRadius: 8,
                    padding: 8,
                    marginBottom: 4,
                    borderWidth: 1,
                    borderColor: "#e5e7eb",
                  }}
                >
                  <Text
                    style={{
                      fontSize: 11,
                      fontWeight: "600",
                      textTransform: "uppercase",
                      color: "#4b5563",
                    }}
                  >
                    {doc.document_type}
                  </Text>
                  <Text style={{ fontSize: 11, color: "#6b7280" }}>
                    {doc.value}
                  </Text>
                  <Text style={{ fontSize: 10, color: "#6b7280", marginTop: 2 }}>
                    {doc.reason}
                  </Text>
                </View>
              ))}
            </View>
          )}
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
