// ─── Sandbox: Moveable Alphabet ──────────────────────────────────────────────
// Analogy: Discovery-driven letter tiles moved physically to spell words.
// Each LetterTile is a moveable React component unit.

import { useState } from "react";

function LetterTile({ letter, onMoveUp, onMoveDown }) {  // <── EXPLORE: rename
  return (
    <span style={{ border: "1px solid #4f83c2", padding: "0.4rem 0.6rem",
                   borderRadius: "6px", margin: "0.15rem", cursor: "pointer" }}
          title={`Move ${letter}`}>
      {letter}
      <button onClick={onMoveUp}   aria-label="move left">◀</button>
      <button onClick={onMoveDown} aria-label="move right">▶</button>
    </span>
  );
}

export default function App() {
  const [letters, setLetters] = useState(["P","Y","T","H","O","N"]);

  const move = (i, dir) => {             // <── EXPLORE: also allow drag-drop
    const j = i + dir;
    if (j < 0 || j >= letters.length) return;
    const arr = [...letters];
    [arr[i], arr[j]] = [arr[j], arr[i]];
    setLetters(arr);
  };

  return (
    <div style={{ fontFamily: "sans-serif", padding: "2rem" }}>
      <h1>Moveable Alphabet</h1>
      <p style={{ letterSpacing: "0.1rem", fontSize: "1.4rem" }}>
        {letters.join("")}
      </p>
      <div>
        {letters.map((l, i) => (
          <LetterTile key={i} letter={l}
                      onMoveUp={()   => move(i, -1)}
                      onMoveDown={() => move(i, +1)} />
        ))}
      </div>
      {/* CREATE: Add a Reset button that restores original order */}
    </div>
  );
}

