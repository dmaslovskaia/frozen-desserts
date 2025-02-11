require 'rails_helper'

# This spec was generated by rspec-rails when you ran the scaffold generator.
# It demonstrates how one might use RSpec to test the controller code that
# was generated by Rails when you ran the scaffold generator.
#
# It assumes that the implementation code is generated by the rails scaffold
# generator. If you are using any extension libraries to generate different
# controller code, this generated spec may or may not pass.
#
# It only uses APIs available in rails and/or rspec-rails. There are a number
# of tools you can use to make these specs even more expressive, but we're
# sticking to rails and rspec-rails APIs to keep things simple and stable.

RSpec.describe "/desserts", type: :request do
  
  # This should return the minimal set of attributes required to create a valid
  # Dessert. As you add validations to Dessert, be sure to
  # adjust the attributes here as well.
  let(:valid_attributes) {
    skip("Add a hash of attributes valid for your model")
  }

  let(:invalid_attributes) {
    skip("Add a hash of attributes invalid for your model")
  }

  describe "GET /index" do
    it "renders a successful response" do
      Dessert.create! valid_attributes
      get desserts_url
      expect(response).to be_successful
    end
  end

  describe "GET /show" do
    it "renders a successful response" do
      dessert = Dessert.create! valid_attributes
      get dessert_url(dessert)
      expect(response).to be_successful
    end
  end

  describe "GET /new" do
    it "renders a successful response" do
      Dessert.create! valid_attributes
      get new_dessert_url
      expect(response).to be_successful
    end
  end

  describe "GET /edit" do
    it "renders a successful response" do
      dessert = Dessert.create! valid_attributes
      get edit_dessert_url(dessert)
      expect(response).to be_successful
    end
  end

  describe "POST /create" do
    context "with valid parameters" do
      it "creates a new Dessert" do
        expect {
          post desserts_url, params: { dessert: valid_attributes }
        }.to change(Dessert, :count).by(1)
      end

      it "redirects to the created dessert" do
        post desserts_url, params: { dessert: valid_attributes }
        expect(response).to redirect_to(dessert_url(Dessert.last))
      end
    end

    context "with invalid parameters" do
      it "does not create a new Dessert" do
        expect {
          post desserts_url, params: { dessert: invalid_attributes }
        }.to change(Dessert, :count).by(0)
      end

    
      it "renders a response with 422 status (i.e. to display the 'new' template)" do
        post desserts_url, params: { dessert: invalid_attributes }
        expect(response).to have_http_status(:unprocessable_entity)
      end
    
    end
  end

  describe "PATCH /update" do
    context "with valid parameters" do
      let(:new_attributes) {
        skip("Add a hash of attributes valid for your model")
      }

      it "updates the requested dessert" do
        dessert = Dessert.create! valid_attributes
        patch dessert_url(dessert), params: { dessert: new_attributes }
        dessert.reload
        skip("Add assertions for updated state")
      end

      it "redirects to the dessert" do
        dessert = Dessert.create! valid_attributes
        patch dessert_url(dessert), params: { dessert: new_attributes }
        dessert.reload
        expect(response).to redirect_to(dessert_url(dessert))
      end
    end

    context "with invalid parameters" do
    
      it "renders a response with 422 status (i.e. to display the 'edit' template)" do
        dessert = Dessert.create! valid_attributes
        patch dessert_url(dessert), params: { dessert: invalid_attributes }
        expect(response).to have_http_status(:unprocessable_entity)
      end
    
    end
  end

  describe "DELETE /destroy" do
    it "destroys the requested dessert" do
      dessert = Dessert.create! valid_attributes
      expect {
        delete dessert_url(dessert)
      }.to change(Dessert, :count).by(-1)
    end

    it "redirects to the desserts list" do
      dessert = Dessert.create! valid_attributes
      delete dessert_url(dessert)
      expect(response).to redirect_to(desserts_url)
    end
  end
end
