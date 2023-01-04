import Head from "next/head";
import Image from "next/image";
import { Source_Sans_Pro } from "@next/font/google";
import grompFull from "../public/gromp-full.png";

const sourceSansPro = Source_Sans_Pro({
  subsets: ["latin"],
  weight: ["200", "300", "400", "600", "700", "900"],
});

export default function Home() {
  const features = [
    "Live game info",
    "Summoner profiles",
    "Champion info",
    "Challenges",
    "More coming...",
  ];
  return (
    <>
      <Head>
        <title>Gromp, LoL Discord Bot</title>
        <meta name="description" content="Gromp.gg home page" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.png" />
      </Head>

      <main
        className={`flex flex-col h-auto w-screen max-w-none min-h-screen bg-gradient-to-tl from-amber-700 to-lime-500 items-center justify-center ${sourceSansPro.className}`}
      >
        <section className="flex flex-col items-center gap-3">
          <h1 className="text-6xl md:text-8xl text-center font-black">GROMP</h1>
          <h3 className="text-sm md:text-md text-center">Coming soon...</h3>
          <Image src={grompFull} alt="Gromp.gg logo" className="w-36 lg:w-96" />
          <h1 className="text-2xl text-center px-10 md:text-4xl">
            Multipurpose League of Legends Discord Bot.
          </h1>
          <div className="flex flex-col sm:flex-row gap-2">
            {features.map((feature, index) => {
              return (
                <code
                  className="rounded-lg px-2 py-1 bg-lime-300 text-xs lg:text-lg"
                  key={index}
                >
                  {feature}
                </code>
              );
            })}
          </div>
        </section>
      </main>
    </>
  );
}
