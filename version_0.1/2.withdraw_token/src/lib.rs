use scrypto::prelude::*;

//0.DEFINE BLUEPRINT 
blueprint! {
    struct UserVault{
        dinar_vault : Vault,
        radix_vault : Vault,
        price:Decimal
    }

    impl UserVault{
        //1.INSTANTIATE VAULT
        pub fn instantiate_machine(price:Decimal) -> ComponentAddress{
            //1.1.CREATE VAULT RESOOURCE
            let dinar_vault: Bucket = ResourceBuilder::new_fungible()
                .divisibility(DIVISIBILITY_NONE)
                .metadata("name","dinar_vault")
                .metadata("symbol","DIN")
                .initial_supply(300);

            //INSTANTIATE COMPONENT AND RETURN IT 
            Self {
                dinar_vault: Vault::with_bucket(dinar_vault),
                radix_vault: Vault::new(RADIX_TOKEN),
                price: price
            }
            .instantiate().globalize()
        }

        //2.BUY METHOD 
        pub fn buy_dinar(&mut self, mut payment: Bucket) -> (Bucket, Bucket){
            info!("Buying DINAR");

            let our_share=payment.take(self.price);

            self.radix_vault.put(our_share);
            
            let dinar_vault: Bucket =self.dinar_vault.take(1);
            (dinar_vault, payment)

        }
 
        //3. WITHDRAW METHODS
        pub fn withdraw_dinar(&mut self) -> Bucket {
            // Simply take all resources from the collected_xrd vault and
            // return them
            self.dinar_vault.take(1)
        }



        
    }


}