import type { Metadata } from "next";
import "./globals.css";
export const metadata: Metadata = {
  title: "BUFFER OVERFLOW · P11",
  description: "BUFFER OVERFLOW — laboratoire local, éthique, 0 GPU.",
};
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="fr"><body>{children}</body></html>;
}
