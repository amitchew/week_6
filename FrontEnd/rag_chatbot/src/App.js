import { useState } from "react";

import Message from "./components/Message";
import Input from "./components/Input";
import History from "./components/History";
import Clear from "./components/Clear";

import "./App.css";

export default function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [accuracy, setAccuracy] = useState([]);
  const [Classification, setClassification] = useState([]);


  const handleSubmit = async () => {
    const prompt = {
      role: "user",
      content: input
    };

    setMessages([...messages, prompt]);

    await fetch("https://localhost:3001/chat/", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.REACT_APP_OPENAI_API_KEY}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages: [...messages, prompt]
      })
    })
      .then((data) => data.json())
      .then((data) => {
        console.log(data);
        const res = data.choices[0].message.content;
        setMessages((messages) => [
          ...messages,
          {
            role: "assistant",
            content: res
          }
        ]);
        setAccuracy((accuracy) => [
          accuracy = data.choices[0]?.message?.accuracy || " ",
        ]);
        setClassification((classification) => [
          classification = data.choices[0]?.message?.classification || " ",
        ]);
        setHistory((history) => [...history, { question: input, answer: res }]);
        setInput("");
      });
  };

  const clear = () => {
    setMessages([]);
    setHistory([]);
    setAccuracy([]);
    setClassification([]);
  };

  return (
    <div className="App">
      <div className="Column">
        <h3 className="Title">PromptlyTech RAG</h3>
        <div className="Content">
          {messages.map((el, i) => {
            return <Message key={i} role={el.role} content={el.content} />;
          })}
        </div>
        <Input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onClick={input ? handleSubmit : undefined}
        />
      </div>
      <div className="Column">
        {/* <h3 className="Title">History</h3> */}
        <h6 className="Title">Accuracy {accuracy} %</h6>

        <h6 className="Title">Classification {Classification} </h6>




        <div className="Content">
          {history.map((el, i) => {
            return (
              <History
                key={i}
                question={el.question}
                onClick={() =>
                  setMessages([
                    { role: "user", content: history[i].question },
                    { role: "assistant", content: history[i].answer }
                  ])
                }
              />
            );
          })}
        </div>
        <Clear onClick={clear} />
      </div>
    </div>
  );
}
