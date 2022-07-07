use scrypto::prelude::*;

blueprint! {
    struct UserVault {
        dinar_vault: Vault,
        radix_vault: Vault,
        price:Decimal
    }

    impl UserVault {
        //1.INSTANTIATE VAULT
        pub fn instantiate_machine(price: Decimal) -> (ComponentAddress, Bucket) {
            //1.1 ADMIN BADGE
            let admin_badge:Bucket = ResourceBuilder::new_fungible()
                .divisibility(DIVISIBILITY_NONE)
                .metadata("name", "admin_badge")
                .initial_supply(1);

            //1.2 CREATE RESOURCE
            let dinar_vault: Bucket = ResourceBuilder::new_fungible()
                .divisibility(DIVISIBILITY_NONE)
                .metadata("name", "dinar_vault")
                .initial_supply(300);

            //1.3CREATE ACCES RULE 
            let acces_rules = AccessRules::new()
                .method("withdraw_xrd",rule!(require(admin_badge.resource_address())))
                .default(rule!(allow_all));

            //1.4 INSTANTIATE COMPONET AND ADD ACCES RULE 
            let component = Self {
                dinar_vault :Vault::with_bucket(dinar_vault),
                radix_vault : Vault::new(RADIX_TOKEN),
                price : price
            }
            .instantiate()
            .add_access_check(acces_rules);

            //1.5 RETURN ADDRESS AND ADMIN BADGE
            (component.globalize(), admin_badge)
        }

        //2.METHODS

        //2.1 BUY DINAR
        pub fn buy_dinar(&mut self, mut payment: Bucket) -> (Bucket, Bucket){
            let our_share=payment.take(self.price);
            self.radix_vault.put(our_share);
            let dinar_vault:Bucket = self.dinar_vault.take(1);
            (dinar_vault, payment)

        }

        //2.2 WITHDRAW XRD
        pub fn withdraw_xrd(&mut self) -> Bucket{
            self.radix_vault.take_all()
        }

    }

}