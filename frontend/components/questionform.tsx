export default function QuestionForm() {
  return (
    <form id="image-form">   
      <div className="m-4">
          <label className="m-4" htmlFor="question">Your Question:</label>
          <input type="text" id="question" name="question"/>
          <button className="bg-white text-black w-16 m-4" type="submit">Analyze</button>
      </div>
    </form>
  );

}