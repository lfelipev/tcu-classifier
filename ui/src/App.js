import React, { Component } from 'react';
import './App.css';
import Form from 'react-bootstrap/Form';
import Col from 'react-bootstrap/Col';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.css';

class App extends Component {

  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,
      formData: {
        numacordao: 7,
        anoacordao: 2002,
        colegiado: 'Plenário',
        conteudo: '(Opcional)'
      },
      result: ""
    };
  }

  handleChange = (event) => {
    const value = event.target.value;
    const name = event.target.name;
    var formData = this.state.formData;
    formData[name] = value;
    this.setState({
      formData
    });
  }

  handlePredictClick = (event) => {
    const formData = this.state.formData;
    this.setState({ isLoading: true });
    fetch('http://localhost:5000/prediction/', 
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        method: 'POST',
        body: JSON.stringify(formData)
      })
      .then(response => response.json())
      .then(response => {
        this.setState({
          result: response.result,
          isLoading: false
        });
      });
  }

  handleCancelClick = (event) => {
    this.setState({ result: "" });
  }

  render() {
    const isLoading = this.state.isLoading;
    const formData = this.state.formData;
    const result = this.state.result;
    return (
      <Container>
        <div>
          <h1 className="title">Classificador de Assuntos de Acórdãos</h1>
        </div>
        <div className="content">
          <Form>
            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>Número do Acórdão</Form.Label>
                <Form.Control 
                  value={formData.numacordao}
                  type="text"
                  name="numacordao"
                  onChange={this.handleChange}>
                </Form.Control>
              </Form.Group>
              <Form.Group as={Col}>
                <Form.Label>Ano do Acórdão</Form.Label>
                <Form.Control 
                  type="text"
                  value={formData.anoacordao}
                  name="anoacordao"
                  onChange={this.handleChange}>
                </Form.Control>
              </Form.Group>
            </Form.Row>
            <Form.Row>
              <Form.Group as={Col}>
                <Form.Label>Colegiado</Form.Label>
                <Form.Control 
                  type="text"
                  value={formData.colegiado}
                  name="colegiado"
                  onChange={this.handleChange}>
                </Form.Control>
              </Form.Group>

              <Form.Group as={Col}>
                <Form.Label>Conteúdo do Acórdão</Form.Label>
                <Form.Control 
                  type="text"
                  value={formData.conteudo}
                  name="conteudo"
                  onChange={this.handleChange}>
                </Form.Control>
              </Form.Group>

            </Form.Row>
            <Row>
              <Col>
                <Button
                  block
                  variant="success"
                  disabled={isLoading}
                  onClick={!isLoading ? this.handlePredictClick : null}>
                  { isLoading ? 'PREDIZENDO ASSUNTO' : 'PREDIZER' }
                </Button>
              </Col>
              <Col>
                <Button
                  block
                  variant="danger"
                  disabled={isLoading}
                  onClick={this.handleCancelClick}>
                  RESETAR PREDIÇÃO
                </Button>
              </Col>
            </Row>
          </Form>
          {result === "" ? null :
            (<Row>
              <Col className="result-container">
                <h5 id="result">{result}</h5>
              </Col>
            </Row>)
          }
        </div>
      </Container>
    );
  }
}

export default App;